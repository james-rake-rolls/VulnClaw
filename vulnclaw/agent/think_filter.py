"""VulnClaw Think Tag Filter — strip <think>/<thinking> blocks from LLM output.

Modified by: Nyaecho
Modified: 2026-07-08
Reason: V2 fix — the pure text helper functions moved to config/text_utils.py; re-exported here for
         agent/-layer backward compatibility.
"""

from __future__ import annotations

from vulnclaw.config.text_utils import format_think_tags, strip_think_tags  # noqa: F401

__all__ = ["strip_think_tags", "format_think_tags"]
