"""URL utility functions — shared across infrastructure and domain layers.

Modified by: Nyaecho
Modified: 2026-07-08
Reason: eliminate a V1 violation — the mcp/lifecycle.py infrastructure layer should not depend back on
         the agent/builtin_tools.py domain layer; the pure URL helpers were extracted into the
         config/ infrastructure package.
"""

from __future__ import annotations

from urllib.parse import urlparse


def infer_port_from_url(url: str) -> int | None:
    """Infer request port from URL.

    Returns the explicit port if present in the URL, otherwise infers
    from the scheme (443 for https, 80 for http), or None if unknown.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return None
    if parsed.port:
        return parsed.port
    if parsed.scheme == "https":
        return 443
    if parsed.scheme == "http":
        return 80
    return None
