"""Bilingual skill-loading tests — SKILL.<lang>.md / references/*.<lang>.md.

Covers the language-variant resolution added to ``vulnclaw.skills.loader``:
English content is served when a ``.en.md`` sibling exists, the Chinese base is
the fallback, structural frontmatter never drifts, and language siblings stay
out of the advertised reference list.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import vulnclaw.skills.loader as loader


@pytest.fixture()
def skill_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A specialized skill with base (zh) files and partial English variants."""
    root = tmp_path / "specialized"
    skill = root / "demo-skill"
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: demo-skill\n"
        "description: 中文描述\n"
        "requires_target: false\n"
        "routing:\n"
        "  keywords: [demo]\n"
        "---\n"
        "中文正文",
        encoding="utf-8",
    )
    (skill / "SKILL.en.md").write_text(
        "---\nname: demo-skill\ndescription: English description\n---\nEnglish body",
        encoding="utf-8",
    )
    (skill / "references" / "guide.md").write_text("中文参考", encoding="utf-8")
    (skill / "references" / "guide.en.md").write_text("English reference", encoding="utf-8")
    # A reference with no English variant yet — must fall back to Chinese.
    (skill / "references" / "only-zh.md").write_text("只有中文", encoding="utf-8")

    monkeypatch.setattr(loader, "_SPECIALIZED_SKILLS_DIR", root)
    return root


def test_zh_serves_base_files(skill_dir: Path) -> None:
    skill = loader.load_specialized_skill("demo-skill", lang="zh")
    assert skill is not None
    assert skill["description"] == "中文描述"
    assert skill["content"] == "中文正文"


def test_en_serves_variant_when_present(skill_dir: Path) -> None:
    skill = loader.load_specialized_skill("demo-skill", lang="en")
    assert skill is not None
    assert skill["description"] == "English description"
    assert skill["content"] == "English body"


def test_structural_frontmatter_never_drifts(skill_dir: Path) -> None:
    # requires_target / routing come from the base SKILL.md even when the English
    # variant omits them.
    en = loader.load_specialized_skill("demo-skill", lang="en")
    assert en["requires_target"] is False
    assert en["routing"] == {"keywords": ["demo"]}
    assert en["format"] == "directory"


def test_reference_list_hides_language_variants(skill_dir: Path) -> None:
    skill = loader.load_specialized_skill("demo-skill", lang="en")
    assert skill["references"] == ["guide.md", "only-zh.md"]
    assert "guide.en.md" not in skill["references"]


def test_reference_resolution_prefers_active_language(skill_dir: Path) -> None:
    assert loader.load_skill_reference("demo-skill", "guide.md", lang="en") == "English reference"
    assert loader.load_skill_reference("demo-skill", "guide.md", lang="zh") == "中文参考"


def test_reference_falls_back_to_base_when_untranslated(skill_dir: Path) -> None:
    # No only-zh.en.md exists → English request still gets the Chinese base.
    assert loader.load_skill_reference("demo-skill", "only-zh.md", lang="en") == "只有中文"


def test_explicit_variant_name_is_accepted(skill_dir: Path) -> None:
    # A caller passing the concrete variant name still resolves.
    assert loader.load_skill_reference("demo-skill", "guide.en.md", lang="en") == "English reference"


def test_default_language_follows_current_lang(
    skill_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import vulnclaw.i18n as i18n

    monkeypatch.setenv("VULNCLAW_LANG", "en")
    i18n._translator = None  # force re-detection
    try:
        skill = loader.load_specialized_skill("demo-skill")
        assert skill["description"] == "English description"
    finally:
        i18n._translator = None
