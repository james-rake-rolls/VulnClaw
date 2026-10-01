"""Constraint policy helpers for task, phase, and tool enforcement."""

from __future__ import annotations

# Modified by: Nyaecho
# Modified: 2026-07-08
# Reason: eliminate V2/V3/V4 violations — leaf types moved to config/domain_models.py,
#          import and re-export the shared policy functions from config here.
from vulnclaw.config.domain_models import (
    PHASE_TO_ACTION,
    PentestPhase,
    TaskConstraints,
    normalize_action_name,
    phase_display_name,
    validate_action_constraints,
)

# Re-export for backward compatibility
__all__ = [
    "PHASE_TO_ACTION",
    "PentestPhase",
    "TaskConstraints",
    "normalize_action_name",
    "validate_action_constraints",
    "validate_phase_transition",
    "validate_tool_action",
    "infer_tool_action",
]


def validate_phase_transition(
    next_phase: PentestPhase,
    constraints: TaskConstraints,
) -> str | None:
    """Return a constraint violation message when a phase transition is out of scope."""
    action = PHASE_TO_ACTION.get(next_phase)
    if action is None:
        return None
    violation = validate_action_constraints(action, constraints)
    if violation is None:
        return None
    return f"{violation} (phase transition to {phase_display_name(next_phase)})"


# Pure local/knowledge tools: do not interact with the target, excluded from the "action scope" constraint
LOCAL_META_TOOLS = {
    "evidence_list",
    "evidence_search",
    "evidence_view",
    "load_skill_reference",
    "crypto_decode",
    "source_extract",
    "runtime_diff_probe",
    "agent_run",
    "agent_job",
}

# Payload signatures that truly indicate "exploitation" intent — independent of transport (HTTP method / network library)
EXPLOIT_PAYLOAD_MARKERS = [
    "union select",
    " or 1=1",
    "'or'",
    "../",
    "..\\",
    "<script",
    "cmd=",
    "php://",
    "data://",
    "extractvalue(",
    "updatexml(",
    "load_file(",
    "into outfile",
    "{{",  # SSTI
    "${",  # SSTI/EL
    "%00",
    "/etc/passwd",
    "/bin/sh",
    "bash -i",
    "nc -e",
    "powershell -e",
]

# Signatures of local command execution / reverse shell inside python_execute
PYTHON_EXPLOIT_MARKERS = [
    "os.system",
    "subprocess",
    "pty.spawn",
    "/bin/sh",
    "bash -i",
    "nc -e",
    "reverse_shell",
]


def infer_tool_action(tool_name: str, args: dict[str, object]) -> str:
    """Infer the effective action class of a tool invocation.

    Key principle: only an "actual attack payload" is inferred as exploit; the HTTP method and
    whether requests/urllib is used are transport details that do not constitute exploitation intent
    (the recon/scan phases legitimately need to send POST/OPTIONS and probe with requests).
    """
    normalized_tool = (tool_name or "").strip().lower()

    if normalized_tool in LOCAL_META_TOOLS:
        return "recon"  # Local-only operations, exempted together with validate_tool_action

    # Intel tools: read-only lookups (no target egress) and active recon
    # (low-impact target/3rd-party contact) both classify as passive "recon".
    from vulnclaw.intel.tools import READ_ONLY_INTEL_TOOLS, RECON_INTEL_TOOLS

    if normalized_tool in READ_ONLY_INTEL_TOOLS or normalized_tool in RECON_INTEL_TOOLS:
        return "recon"

    if normalized_tool == "nmap_scan":
        return "recon"

    if normalized_tool == "fetch":
        url = str(args.get("url", "") or "").lower()
        method = str(args.get("method", "GET") or "GET").upper()
        payload_surface = " ".join(
            str(args.get(key, "") or "").lower()
            for key in ("body", "data", "form", "json", "params", "headers")
        )
        if any(marker in url or marker in payload_surface for marker in EXPLOIT_PAYLOAD_MARKERS):
            return "exploit"
        # The method alone is not exploitation: GET/HEAD/OPTIONS are recon, others (POST form testing, etc.) are scanning
        if method in ("GET", "HEAD", "OPTIONS"):
            return "recon"
        return "scan"

    if normalized_tool == "http_probe_batch":
        requests = args.get("requests", [])
        if not isinstance(requests, list):
            requests = []
        joined_parts: list[str] = []
        methods: list[str] = []
        for item in requests:
            if not isinstance(item, dict):
                continue
            methods.append(str(item.get("method", "GET") or "GET").upper())
            for key in ("url", "raw_url", "params", "data", "body", "json"):
                joined_parts.append(str(item.get(key, "") or "").lower())
        joined = " ".join(joined_parts)
        if any(marker in joined for marker in EXPLOIT_PAYLOAD_MARKERS):
            return "exploit"
        if all(method in ("GET", "HEAD", "OPTIONS") for method in methods or ["GET"]):
            return "recon"
        return "scan"

    if normalized_tool == "python_execute":
        code = str(args.get("code", "") or "").lower()
        if any(marker in code for marker in EXPLOIT_PAYLOAD_MARKERS + PYTHON_EXPLOIT_MARKERS):
            return "exploit"
        # HTTP probing via requests/httpx/urllib/socket is scanning, not exploitation
        if any(m in code for m in ("requests.", "httpx.", "urllib", "http.client", "socket")):
            return "scan"
        return "recon"

    if normalized_tool == "shell_command":
        command = str(args.get("command", "") or args.get("cmd", "") or "").lower()
        if any(marker in command for marker in EXPLOIT_PAYLOAD_MARKERS + PYTHON_EXPLOIT_MARKERS):
            return "exploit"
        if any(
            marker in command
            for marker in (
                "curl ",
                "wget ",
                "invoke-webrequest",
                "invoke-restmethod",
                "iwr ",
                "irm ",
                "http://",
                "https://",
            )
        ):
            return "scan"
        return "recon"

    if normalized_tool == "brute_force_login":
        return "scan"

    return "scan"


def validate_tool_action(
    tool_name: str, args: dict[str, object], constraints: TaskConstraints
) -> str | None:
    """Return a constraint violation when a tool invocation implies a blocked action."""
    # Pure local/knowledge tools are not bound by the action scope (loading docs, encoding/decoding do not touch the target)
    if (tool_name or "").strip().lower() in LOCAL_META_TOOLS:
        return None
    inferred = infer_tool_action(tool_name, args)
    violation = validate_action_constraints(inferred, constraints)
    if violation is None:
        return None
    return f"{violation} (tool '{tool_name}' inferred action '{inferred}')"
