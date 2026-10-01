"""MCP diagnostics schemas — shared view models for MCP service state.

Modified by: Nyaecho
Modified: 2026-07-08
Reason: eliminate a V6 violation — the MCP diagnostics views were extracted from web/schemas.py into the
         mcp/ package so both the CLI and Web entry layers can obtain diagnostics from the infrastructure layer.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class MCPServiceView(BaseModel):
    """View model for a single MCP service's state."""

    name: str
    enabled: bool
    priority: int
    transport_type: str
    execution_mode: str
    health_status: str
    attach_attempted: bool = False
    attach_succeeded: bool = False
    running: bool
    can_execute: bool
    tool_count: int = 0
    tools: list[str] = Field(default_factory=list)
    error: Optional[str] = None
    last_error_type: Optional[str] = None
    started_at: Optional[str] = None
    description: str = ""
    call_count: int = 0
    success_count: int = 0
    failure_count: int = 0


class MCPDiagnosticsView(BaseModel):
    """View model for aggregated MCP diagnostics."""

    total_services: int = 0
    running_services: int = 0
    local_services: int = 0
    placeholder_services: int = 0
    tool_count: int = 0
    services: list[MCPServiceView] = Field(default_factory=list)
