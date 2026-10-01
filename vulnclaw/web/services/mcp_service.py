"""MCP diagnostics service for the Web UI backend.

Modified by: Nyaecho
Modified: 2026-07-08
Reason: V6 fix — get_mcp_diagnostics moved to mcp/diagnostics.py; re-exported here for web-layer
         backward compatibility.
"""

from __future__ import annotations

from vulnclaw.mcp.diagnostics import get_mcp_diagnostics  # noqa: F401
from vulnclaw.mcp.schemas import MCPDiagnosticsView, MCPServiceView  # noqa: F401
