"""VulnClaw Skill Loader — load and parse Skill definition files.

Supports two Skill formats:
- Directory format: <skill_name>/SKILL.md + <skill_name>/references/
- Flat file format: <skill_name>.md (legacy, auto-migrated)

Bilingual content
-----------------
Skill text (the ``SKILL.md`` body/description and every file under
``references/``) can ship a per-language variant beside the base file, named
``<stem>.<lang>.md`` (e.g. ``SKILL.en.md``, ``web-sqli.en.md``). The base file
stays authoritative for structure (name / ``requires_target`` / ``routing``) and
is the fallback content; when the active UI language (``vulnclaw.i18n``) has a
matching variant, its body/description is served instead. This lets English be
added incrementally on top of the existing Chinese corpus without a hard cut
over: an untranslated reference simply serves its Chinese base until a
``.en.md`` sibling is added.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from vulnclaw.config.settings import SKILLS_DIR

# ── Built-in skills directory ───────────────────────────────────────

_CORE_SKILLS_DIR = Path(__file__).parent / "core"
_SPECIALIZED_SKILLS_DIR = Path(__file__).parent / "specialized"

# Languages that may appear as ``<stem>.<lang>.md`` content variants. ``zh`` is
# the authoring language of the base files, so a bare ``<stem>.md`` *is* the
# Chinese variant; only non-``zh`` codes are looked up as siblings.
_KNOWN_LANGS = frozenset({"en", "zh"})


def _active_lang(lang: Optional[str]) -> str:
    """Resolve the effective UI language ('zh'/'en'), defaulting to the global.

    Kept lazy (imported inside the function) so the loader has no import-time
    dependency on the i18n singleton and stays trivially testable via an
    explicit ``lang`` argument.
    """
    if lang:
        return lang
    try:
        from vulnclaw.i18n import current_lang

        return current_lang()
    except Exception:
        return "zh"


def _lang_variant(path: Path, lang: Optional[str]) -> Path:
    """Return the ``<stem>.<lang>.md`` sibling of ``path`` when it exists.

    Falls back to ``path`` itself for the base/authoring language ('zh'), when
    no variant is present, or for non-markdown references. This is a pure
    filesystem resolution and never raises for a missing file.
    """
    resolved = _active_lang(lang)
    if resolved == "zh" or resolved not in _KNOWN_LANGS:
        return path
    if path.suffix != ".md":
        return path
    candidate = path.parent / f"{path.stem}.{resolved}.md"
    if candidate.exists() and candidate.is_file():
        return candidate
    return path


def _is_lang_variant_name(filename: str) -> bool:
    """True for a ``<stem>.<lang>.md`` reference variant (e.g. ``foo.en.md``).

    Used to keep language siblings out of the advertised reference list so the
    catalog exposes stable, language-agnostic base names only.
    """
    p = Path(filename)
    if p.suffix != ".md":
        return False
    inner_suffix = p.stem.rsplit(".", 1)
    return len(inner_suffix) == 2 and inner_suffix[1] in _KNOWN_LANGS


def _is_directory_skill(path: Path) -> bool:
    """Check if a path is a directory-format skill (has SKILL.md)."""
    return path.is_dir() and (path / "SKILL.md").exists()


def _is_flat_skill(path: Path) -> bool:
    """Check if a path is a flat-file skill (.md file directly)."""
    return path.is_file() and path.suffix == ".md"


def load_core_skill(name: str, lang: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Load a core skill by name.

    Args:
        name: Skill name, e.g. "pentest-flow"
        lang: Optional language override ('zh'/'en'); defaults to the active UI
            language. English content is served when a ``.en.md`` variant exists,
            otherwise the Chinese base is used.

    Returns:
        Dict with keys: name, description, content, path, references
        Or None if not found.
    """
    # Try directory format first
    skill_dir = _CORE_SKILLS_DIR / name
    if _is_directory_skill(skill_dir):
        return _parse_skill_directory(skill_dir, lang)

    # Fall back to flat file format
    skill_file = _CORE_SKILLS_DIR / f"{name}.md"
    if _is_flat_skill(skill_file):
        return _parse_skill_file(_lang_variant(skill_file, lang), base_path=skill_file)

    return None


def load_specialized_skill(name: str, lang: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Load a specialized skill by name."""
    # Try directory format first
    skill_dir = _SPECIALIZED_SKILLS_DIR / name
    if _is_directory_skill(skill_dir):
        return _parse_skill_directory(skill_dir, lang)

    # Fall back to flat file format
    skill_file = _SPECIALIZED_SKILLS_DIR / f"{name}.md"
    if _is_flat_skill(skill_file):
        return _parse_skill_file(_lang_variant(skill_file, lang), base_path=skill_file)

    return None


def load_custom_skill(name: str, lang: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Load a user custom skill by name."""
    # Try directory format first
    skill_dir = SKILLS_DIR / name
    if _is_directory_skill(skill_dir):
        return _parse_skill_directory(skill_dir, lang)

    # Fall back to flat file format
    skill_file = SKILLS_DIR / f"{name}.md"
    if _is_flat_skill(skill_file):
        return _parse_skill_file(_lang_variant(skill_file, lang), base_path=skill_file)

    return None


def list_core_skills() -> list[str]:
    """List all available core skill names."""
    if not _CORE_SKILLS_DIR.exists():
        return []
    names = set()
    for child in _CORE_SKILLS_DIR.iterdir():
        if _is_directory_skill(child):
            names.add(child.name)
        elif (
            _is_flat_skill(child)
            and child.suffix == ".md"
            and not _is_lang_variant_name(child.name)
        ):
            names.add(child.stem)
    return sorted(names)


def list_specialized_skills() -> list[str]:
    """List all available specialized skill names."""
    if not _SPECIALIZED_SKILLS_DIR.exists():
        return []
    names = set()
    for child in _SPECIALIZED_SKILLS_DIR.iterdir():
        if _is_directory_skill(child):
            names.add(child.name)
        elif (
            _is_flat_skill(child)
            and child.suffix == ".md"
            and not _is_lang_variant_name(child.name)
        ):
            names.add(child.stem)
    return sorted(names)


def list_custom_skills() -> list[str]:
    """List all available custom skill names."""
    if not SKILLS_DIR.exists():
        return []
    names = set()
    for child in SKILLS_DIR.iterdir():
        if _is_directory_skill(child):
            names.add(child.name)
        elif (
            _is_flat_skill(child)
            and child.suffix == ".md"
            and not _is_lang_variant_name(child.name)
        ):
            names.add(child.stem)
    return sorted(names)


def load_skill_by_name(name: str, lang: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Load a skill by name, searching core → specialized → custom."""
    for loader in [load_core_skill, load_specialized_skill, load_custom_skill]:
        result = loader(name, lang)
        if result:
            return result
    return None


def _parse_skill_directory(skill_dir: Path, lang: Optional[str] = None) -> dict[str, Any]:
    """Parse a directory-format skill.

    Directory structure:
        <skill_name>/
        ├── SKILL.md          (required, base/Chinese)
        ├── SKILL.en.md       (optional English variant)
        └── references/       (optional)
            ├── ref1.md       (base/Chinese)
            ├── ref1.en.md    (optional English variant)
            └── ref2.md

    Structural frontmatter (name / requires_target / routing) always comes from
    the base ``SKILL.md`` so the two language files cannot drift; only the
    human-readable ``description`` and body are taken from the active-language
    variant when one exists.
    """
    base_skill_file = skill_dir / "SKILL.md"
    result = _parse_skill_file(base_skill_file)

    # Overlay the active-language SKILL body/description when a variant exists.
    lang_skill_file = _lang_variant(base_skill_file, lang)
    if lang_skill_file != base_skill_file:
        variant = _parse_skill_file(lang_skill_file, base_path=base_skill_file)
        result["content"] = variant["content"]
        if variant.get("description"):
            result["description"] = variant["description"]

    # Collect reference files, hiding language-variant siblings so the catalog
    # advertises stable base names only (``load_skill_reference`` resolves the
    # active-language body transparently).
    references_dir = skill_dir / "references"
    ref_files: list[str] = []
    if references_dir.exists() and references_dir.is_dir():
        for ref in sorted(references_dir.iterdir()):
            if ref.suffix in (".md", ".yaml", ".yml") and not _is_lang_variant_name(ref.name):
                ref_files.append(ref.name)

    result["references"] = ref_files
    result["references_dir"] = str(references_dir)
    result["skill_dir"] = str(skill_dir)
    result["format"] = "directory"

    return result


def _parse_skill_file(path: Path, base_path: Optional[Path] = None) -> dict[str, Any]:
    """Parse a skill markdown file.

    Skill files use a simple format:
    - Optional YAML frontmatter (between --- markers)
    - Markdown body with skill content

    ``base_path`` is the authoring (base-language) file this one is a variant of;
    when given, the skill ``name`` and ``skill_dir`` derive from the base so an
    English variant such as ``SKILL.en.md`` or ``web-sqli.en.md`` keeps the base
    skill's identity instead of picking up the ``.en`` filename.
    """
    content = path.read_text(encoding="utf-8")
    name_path = base_path or path
    name = name_path.stem if name_path.name != "SKILL.md" else name_path.parent.name

    # Parse optional frontmatter
    description = ""
    # Whether a preset scan target is required before the skill can launch.
    # Self-discovering skills (e.g. ``hackerone``, which reads its target from a
    # scope link) set ``requires_target: false`` in frontmatter to launch
    # target-less. Defaults to True so every existing skill is unchanged.
    requires_target = True
    # Optional typed routing metadata (see vulnclaw.skills.routing). Kept as the
    # raw frontmatter mapping here; the resolver normalizes/validates it into a
    # ``SkillRouting`` model so the loader stays free of routing-schema imports.
    routing: dict[str, Any] = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml

            try:
                frontmatter = yaml.safe_load(parts[1])
                if isinstance(frontmatter, dict):
                    description = frontmatter.get("description", "")
                    name = frontmatter.get("name", name)
                    # Only an explicit boolean ``false`` opts out of the target
                    # gate. Any other value (missing, null, 0, "false", …) keeps
                    # the safe default so malformed frontmatter can't silently
                    # bypass the authorized-target check.
                    rt = frontmatter.get("requires_target", True)
                    requires_target = rt if isinstance(rt, bool) else True
                    raw_routing = frontmatter.get("routing")
                    if isinstance(raw_routing, dict):
                        routing = raw_routing
            except yaml.YAMLError:
                pass
            body = parts[2].strip()

    return {
        "name": name,
        "description": description,
        "content": body,
        "path": str(path),
        "requires_target": requires_target,
        "routing": routing,
        "references": [],
        "references_dir": "",
        "skill_dir": str(name_path.parent) if name_path.name == "SKILL.md" else "",
        "format": "directory" if name_path.name == "SKILL.md" else "flat",
    }


def load_skill_reference(
    skill_name: str, ref_name: str, lang: Optional[str] = None
) -> Optional[str]:
    """Load a reference file from a skill's references directory.

    Args:
        skill_name: The skill name
        ref_name: The reference file name (e.g. "02-client-api-reverse-and-burp.md")
        lang: Optional language override ('zh'/'en'); defaults to the active UI
            language. When the active language has a ``<stem>.<lang>.md`` variant
            beside the requested reference, that variant's content is returned;
            otherwise the base (Chinese) file is served as a fallback.

    Returns:
        The reference file content as string, or None if not found.
    """
    skill = load_skill_by_name(skill_name, lang)
    if not skill or not skill.get("references_dir"):
        return None

    references_dir = Path(skill["references_dir"])
    # Accept either a base name (catalog default) or an explicit variant name.
    base_ref = references_dir / ref_name
    ref_path = _lang_variant(base_ref, lang)
    if ref_path.exists() and ref_path.is_file():
        return ref_path.read_text(encoding="utf-8")
    if base_ref.exists() and base_ref.is_file():
        return base_ref.read_text(encoding="utf-8")

    return None
