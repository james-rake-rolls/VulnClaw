"""VulnClaw Finding Similarity — lightweight semantic deduplication.

A pure-Python semantic dedup for findings, with no external NLP libraries.

Modified by: Nyaecho
Modified: 2026-07-08
Reason: V2 fix — moved from agent/finding_similarity.py to the config/ infrastructure layer,
         removing report/filter.py's dependency on agent/.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional
from urllib.parse import parse_qs, urlsplit

if TYPE_CHECKING:
    from vulnclaw.config.domain_models import VulnerabilityFinding


# ── Vulnerability-type normalization map ───────────────────────────────────────────────────

# Alias -> canonical type. Keys are lowercased and whitespace-stripped.
_VULN_TYPE_ALIASES: dict[str, str] = {
    # SQL injection
    "sqli": "sql_injection",
    "sql注入": "sql_injection",
    "sql injection": "sql_injection",
    "blind sqli": "sql_injection",
    "盲注": "sql_injection",
    "注入漏洞": "sql_injection",
    "sql_injection": "sql_injection",
    # XSS
    "xss": "cross_site_scripting",
    "跨站脚本": "cross_site_scripting",
    "反射型xss": "cross_site_scripting",
    "存储型xss": "cross_site_scripting",
    "xss跨站脚本": "cross_site_scripting",
    "cross site scripting": "cross_site_scripting",
    "cross_site_scripting": "cross_site_scripting",
    # SSRF
    "ssrf": "server_side_request_forgery",
    "服务端请求伪造": "server_side_request_forgery",
    "server side request forgery": "server_side_request_forgery",
    "server_side_request_forgery": "server_side_request_forgery",
    # RCE
    "rce": "remote_code_execution",
    "命令执行": "remote_code_execution",
    "远程代码执行": "remote_code_execution",
    "命令注入": "remote_code_execution",
    "remote code execution": "remote_code_execution",
    "remote_code_execution": "remote_code_execution",
    # LFI / file inclusion
    "lfi": "local_file_inclusion",
    "文件包含": "local_file_inclusion",
    "rfi": "local_file_inclusion",
    "路径遍历": "local_file_inclusion",
    "文件包含/遍历": "local_file_inclusion",
    "local file inclusion": "local_file_inclusion",
    "local_file_inclusion": "local_file_inclusion",
    # IDOR / broken access control
    "idor": "insecure_direct_object_reference",
    "越权": "insecure_direct_object_reference",
    "横向越权": "insecure_direct_object_reference",
    "纵向越权": "insecure_direct_object_reference",
    "insecure direct object reference": "insecure_direct_object_reference",
    "insecure_direct_object_reference": "insecure_direct_object_reference",
    # CSRF
    "csrf": "cross_site_request_forgery",
    "跨站请求伪造": "cross_site_request_forgery",
    "cross site request forgery": "cross_site_request_forgery",
    # Authentication bypass
    "认证绕过": "auth_bypass",
    "未授权": "auth_bypass",
    "未授权访问": "auth_bypass",
    "未认证": "auth_bypass",
    "无需认证": "auth_bypass",
    # Information disclosure
    "信息泄露": "info_disclosure",
    "数据泄露": "info_disclosure",
    "敏感信息泄露": "info_disclosure",
    "info disclosure": "info_disclosure",
}


def normalize_vuln_type(vuln_type: str) -> str:
    """Normalize a vulnerability type, mapping common aliases to a canonical name.

    Args:
        vuln_type: raw vulnerability-type string (any case / language / with spaces).

    Returns:
        the normalized type; when no alias matches, returns the whitespace-stripped lowercase original.
    """
    if not vuln_type:
        return ""
    key = re.sub(r"\s+", " ", vuln_type.strip().lower())
    if key in _VULN_TYPE_ALIASES:
        return _VULN_TYPE_ALIASES[key]
    # Try swapping underscores/spaces, then match again
    underscore = key.replace(" ", "_")
    if underscore in _VULN_TYPE_ALIASES:
        return _VULN_TYPE_ALIASES[underscore]
    spaced = key.replace("_", " ")
    if spaced in _VULN_TYPE_ALIASES:
        return _VULN_TYPE_ALIASES[spaced]
    return underscore


# ── Text normalization and similarity ───────────────────────────────────────────────────

_URL_RE = re.compile(r'https?://[^\s<>"\')\]]+', re.IGNORECASE)
_TOKEN_RE = re.compile(r"[a-z0-9一-鿿]+", re.IGNORECASE)
# Punctuation boundary tags (e.g. [Auto], [Confirmed]) should be stripped before tokenizing to avoid polluting the token set
_NOISE_TAGS = (
    "[自动]", "[已确认]", "[未验证]",
    "[Auto]", "[Confirmed]", "[Unverified]",
)


def _normalize_url_path(url: str) -> str:
    "Normalize a URL: drop the scheme, drop the trailing slash, keep host+path."
    try:
        parts = urlsplit(url)
    except ValueError:
        return url.lower()
    host = (parts.hostname or "").lower()
    path = parts.path or ""
    if len(path) > 1:
        path = path.rstrip("/")
    return f"{host}{path}"


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, collapse whitespace, normalize embedded URL paths.

    Args:
        text: any free text (description/evidence/title).

    Returns:
        the normalized text.
    """
    if not text:
        return ""
    result = text
    for tag in _NOISE_TAGS:
        result = result.replace(tag, " ")
    # Replace embedded URLs with their normalized host+path form
    result = _URL_RE.sub(lambda m: _normalize_url_path(m.group(0)), result)
    result = result.lower()
    result = re.sub(r"\s+", " ", result).strip()
    return result


def _tokenize(text: str) -> set[str]:
    "Split normalized text into a token set."
    return set(_TOKEN_RE.findall(text))


def text_similarity(a: str, b: str) -> float:
    """Jaccard similarity over token sets.

    Args:
        a: text A.
        b: text B.

    Returns:
        a similarity in [0.0, 1.0]. Returns 1.0 when both are empty; 0.0 when only one is empty.
    """
    na, nb = normalize_text(a), normalize_text(b)
    if not na and not nb:
        return 1.0
    if not na or not nb:
        return 0.0
    ta, tb = _tokenize(na), _tokenize(nb)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0


def url_similarity(a: str, b: str) -> float:
    """Compare the host / path / query-parameter similarity of two URLs.

    Weights: host 0.3 + path 0.4 + query parameter-name set 0.3.
    Non-URL strings fall back to a Jaccard text similarity on the raw text.

    Args:
        a: URL or location string A.
        b: URL or location string B.

    Returns:
        a similarity in [0.0, 1.0].
    """
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0

    pa, pb = urlsplit(a.strip()), urlsplit(b.strip())
    # If neither looks like a URL (no scheme, netloc, or path separator), compare as text
    if not (pa.scheme or pa.netloc) and not (pb.scheme or pb.netloc):
        return text_similarity(a, b)

    # host comparison
    ha, hb = (pa.hostname or "").lower(), (pb.hostname or "").lower()
    if not ha and not hb:
        host_sim = 1.0
    elif not ha or not hb:
        host_sim = 0.0
    else:
        host_sim = 1.0 if ha == hb else 0.0

    # path comparison: Jaccard over "/"-split segments
    seg_a = {s for s in pa.path.split("/") if s}
    seg_b = {s for s in pb.path.split("/") if s}
    if not seg_a and not seg_b:
        path_sim = 1.0
    elif not seg_a or not seg_b:
        path_sim = 0.0
    else:
        path_sim = len(seg_a & seg_b) / len(seg_a | seg_b)

    # query parameter-name set comparison (ignore values; different paging/IDs count as the same endpoint)
    qa = set(parse_qs(pa.query).keys())
    qb = set(parse_qs(pb.query).keys())
    if not qa and not qb:
        query_sim = 1.0
    elif not qa or not qb:
        query_sim = 0.0
    else:
        query_sim = len(qa & qb) / len(qa | qb)

    return host_sim * 0.3 + path_sim * 0.4 + query_sim * 0.3


# ── Combined finding similarity ─────────────────────────────────────────────────

_LOCATION_RE = re.compile(r'(?:https?://[^\s<>"\')\]]+)|(?:/[\w%&=?\-./]+)')


def _extract_location(finding: "VulnerabilityFinding") -> str:
    "Extract the first URL or path from a finding's evidence / description as its location."
    for field in (finding.evidence or "", finding.description or ""):
        if not field:
            continue
        m = _LOCATION_RE.search(field)
        if m:
            return m.group(0)
    return ""


def _vuln_type_similarity(a: str, b: str) -> float:
    "Vulnerability-type similarity: exact match 1.0, normalized match 0.8, otherwise 0.0."
    ra, rb = (a or "").strip().lower(), (b or "").strip().lower()
    if ra and rb and ra == rb:
        return 1.0
    na, nb = normalize_vuln_type(a), normalize_vuln_type(b)
    if na and nb and na == nb:
        return 0.8
    return 0.0


def finding_similarity(a: "VulnerabilityFinding", b: "VulnerabilityFinding") -> float:
    """Compare the overall similarity of two findings.

    Dimension weights:
        - vuln_type:    0.3 (exact match 1.0 / normalized match 0.8)
        - location/URL: 0.4 (extracted from evidence/description, then url_similarity)
        - description:  0.3 (Jaccard over title + description text)

    Args:
        a: finding A.
        b: finding B.

    Returns:
        an overall similarity in [0.0, 1.0].
    """
    type_sim = _vuln_type_similarity(a.vuln_type, b.vuln_type)

    loc_a, loc_b = _extract_location(a), _extract_location(b)
    if not loc_a and not loc_b:
        # Neither has an explicit location — this dimension is not comparable, treated as neutral (no bonus or penalty)
        loc_sim = 0.5
    else:
        loc_sim = url_similarity(loc_a, loc_b)

    desc_a = f"{a.title} {a.description}".strip()
    desc_b = f"{b.title} {b.description}".strip()
    desc_sim = text_similarity(desc_a, desc_b)

    return type_sim * 0.3 + loc_sim * 0.4 + desc_sim * 0.3


# ── Evidence-strength comparison and dedup ───────────────────────────────────────────────────

_EVIDENCE_LEVEL_RANK = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
_LIFECYCLE_RANK = {
    "rejected": 0,
    "candidate": 1,
    "pending_verification": 2,
    "needs_manual_review": 3,
    "verified": 4,
}


def _evidence_strength(finding: "VulnerabilityFinding") -> tuple:
    """Compute a finding's evidence strength, used to decide which to keep on a duplicate.

    Sort key (larger is stronger):
        1. verified first (verified=True)
        2. lifecycle level
        3. evidence level L1-L4
        4. evidence text length (more detailed evidence)
    """
    return (
        1 if finding.verified else 0,
        _LIFECYCLE_RANK.get(finding.lifecycle_status, 1),
        _EVIDENCE_LEVEL_RANK.get(finding.evidence_level, 1),
        len(finding.evidence or ""),
    )


def deduplicate_findings(
    findings: list["VulnerabilityFinding"], threshold: float = 0.75
) -> list["VulnerabilityFinding"]:
    """Semantically deduplicate a list of findings, keeping the side with stronger evidence.

    Iterates findings, comparing each new finding against those already kept; a similarity above the
    threshold marks a duplicate, and the one with higher evidence strength is kept.

    Args:
        findings: the raw finding list.
        threshold: similarity threshold, default 0.75.

    Returns:
        the deduplicated list, preserving first-seen relative order.
    """
    kept: list["VulnerabilityFinding"] = []
    for cand in findings:
        dup_index: Optional[int] = None
        for idx, existing in enumerate(kept):
            if finding_similarity(cand, existing) >= threshold:
                dup_index = idx
                break
        if dup_index is None:
            kept.append(cand)
            continue
        # Duplicate hit: keep the one with stronger evidence
        if _evidence_strength(cand) > _evidence_strength(kept[dup_index]):
            kept[dup_index] = cand
    return kept
