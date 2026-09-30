"""VulnClaw Finding Similarity — lightweight semantic deduplication.

Modified by: Nyaecho
Modified: 2026-07-08
Reason: V2 fix — core logic moved to config/finding_similarity.py; re-exported here for
         agent/-layer backward compatibility.
"""

from __future__ import annotations

from vulnclaw.config.finding_similarity import (  # noqa: F401
    _evidence_strength,
    _extract_location,
    _vuln_type_similarity,
    deduplicate_findings,
    finding_similarity,
    normalize_text,
    normalize_vuln_type,
    text_similarity,
    url_similarity,
)

__all__ = [
    "_evidence_strength",
    "_extract_location",
    "_vuln_type_similarity",
    "normalize_text",
    "normalize_vuln_type",
    "text_similarity",
    "url_similarity",
    "finding_similarity",
    "deduplicate_findings",
]
