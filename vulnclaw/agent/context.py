"""VulnClaw session context management — track pentest state across turns."""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import AliasChoices, BaseModel, Field, PrivateAttr

from vulnclaw.agent.agent_state import AgentState
from vulnclaw.agent.reasoning_state import ReasoningState

# ──────────────────────────────────────────────────────────────
# Leaf types were extracted to config/domain_models.py; re-export them here for compatibility.
# Modified by: Nyaecho
# Modified: 2026-07-08
# Reason: eliminate V2/V3/V4 violations — the infrastructure layer should not depend back on the domain layer.
# ──────────────────────────────────────────────────────────────
from vulnclaw.config.domain_models import (  # noqa: F401 — re-export
    PHASE_TO_ACTION,
    ConstraintViolationEvent,
    EvidenceKind,
    EvidenceRef,
    PentestPhase,
    StepRecord,
    StepStatus,
    TaskConstraints,
    VulnerabilityFinding,
    normalize_action_name,
    phase_canonical_id,
    phase_display_name,
    phase_from_canonical_id,
    validate_action_constraints,
)
from vulnclaw.i18n import _, bi as _rl

logger = logging.getLogger(__name__)

# ==============================================================================
# [P17 refactor] Sub-state class definitions
# Modified by: Nyaecho
# Modified: 2026-07-08
# Reason: SessionState had too many fields (20+), violating the single-responsibility principle
#          split into 6 sub-state classes, each owning one clear responsibility domain
# Note: these sub-state classes are held by SessionState via composition,
#          external code accesses them through @property proxies, keeping backward compatibility
# ==============================================================================

class SessionConfig(BaseModel):
    """Basic session configuration — manages the session lifecycle and target information.

    Responsibilities:
    - Session target (target)
    - Current phase (phase)
    - Timestamp (started_at)
    - Resume information (resume_summary, resume_meta)
    - Task constraints (task_constraints)
    """

    target: Optional[str] = None
    phase: PentestPhase = PentestPhase.IDLE
    started_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    resume_summary: str = Field(default="", description="Historical-results summary injected on resume")
    resume_meta: dict[str, Any] = Field(default_factory=dict, description="Resume metadata")
    task_constraints: TaskConstraints = Field(default_factory=TaskConstraints)


class VulnerabilityStore(BaseModel):
    """Finding query view — filters findings by verification/lifecycle status.

    Responsibilities:
    - Finding list (findings): written and synced by SessionState
    - ID cache for exact dedup (_finding_ids_cache)

    Note:
    The only implementation of adding and deduping lives in ``SessionState.add_finding``. This class
    only provides read-only categorized queries (get_verified/pending/...), invoked by ``SessionState``.
    """

    target: Optional[str] = None
    findings: list[VulnerabilityFinding] = Field(default_factory=list)
    semantic_dedup_threshold: float = Field(
        default=0.75, description="Similarity threshold for semantic dedup (0-1)"
    )
    # PrivateAttr is not subject to Pydantic field-naming rules; used for internal dedup tracking
    _finding_ids_cache: set[str] = PrivateAttr(default_factory=set)

    def get_verified_findings(self) -> list[VulnerabilityFinding]:
        "Get the list of verified findings."
        return [f for f in self.findings if f.verified]

    def get_rejected_findings(self) -> list[VulnerabilityFinding]:
        "Get the list of rejected findings (false positives)."
        return [f for f in self.findings if f.verification_status == "rejected"]

    def get_pending_findings(self) -> list[VulnerabilityFinding]:
        "Get the list of pending (to-be-verified) findings."
        return [f for f in self.findings if f.verification_status == "pending"]

    def get_candidate_findings(self) -> list[VulnerabilityFinding]:
        "Get the low-confidence candidate findings."
        return [f for f in self.findings if f.lifecycle_status == "candidate"]

    def get_pending_verification_findings(self) -> list[VulnerabilityFinding]:
        "Get findings that have evidence pending verification."
        return [f for f in self.findings if f.lifecycle_status == "pending_verification"]

    def get_manual_review_findings(self) -> list[VulnerabilityFinding]:
        "Get findings that need manual review."
        return [
            f
            for f in self.findings
            if (
                f.lifecycle_status == "needs_manual_review"
                or (
                    not f.verified
                    and f.verification_status != "rejected"
                    and f.severity in {"Critical", "High"}
                    and f.lifecycle_status in {"candidate", "pending_verification"}
                )
            )
        ]


class ReconState(BaseModel):
    """Recon state management — tracks information-gathering progress.

    Responsibilities:
    - Recon data (recon_data)
    - Four-dimension model completion (recon_dimensions_completed)
    - Dimension-four activation state (recon_dimension4_active)

    Four-dimension model:
    - Dimension 1: server info (ports / real IP / OS / middleware / database)
    - Dimension 2: website info (architecture / fingerprint / WAF / sensitive directories / source leaks / neighbor sites / C-segment)
    - Dimension 3: domain info (WHOIS / ICP filing / subdomains / DNS / certificate transparency)
    - Dimension 4: personnel info (conditionally triggered — activated only on an explicit social-engineering need)
    """

    recon_data: dict[str, Any] = Field(default_factory=dict)
    recon_dimensions_completed: dict[str, bool] = Field(
        default_factory=lambda: {
            "server": False,
            "website": False,
            "domain": False,
            "personnel": False,
        },
        description="Four-dimension information-gathering model completion tracking",
    )
    recon_dimension4_active: bool = Field(
        default=False, description="Whether dimension four (personnel info) is activated"
    )

    def add_recon_subdomain(self, subdomain: str) -> None:
        "Record a discovered subdomain into recon_data['subdomains']."
        if "subdomains" not in self.recon_data:
            self.recon_data["subdomains"] = []
        if subdomain and subdomain not in self.recon_data["subdomains"]:
            self.recon_data["subdomains"].append(subdomain)

    def mark_recon_dimension(self, dimension: str) -> None:
        """Mark a recon dimension as completed.

        Args:
            dimension: one of 'server', 'website', 'domain', 'personnel'
        """
        if dimension in self.recon_dimensions_completed:
            self.recon_dimensions_completed[dimension] = True

    def is_recon_complete(self) -> bool:
        """Check whether all active recon dimensions have been completed at least once.

        Dimension four (personnel info) is only checked when activated.
        """
        for dim, completed in self.recon_dimensions_completed.items():
            if dim == "personnel" and not self.recon_dimension4_active:
                continue
            if not completed:
                return False
        return True

    def get_recon_status_text(self) -> str:
        "Get a human-readable recon-dimension completion status."

        parts = []
        for dim, completed in self.recon_dimensions_completed.items():
            if dim == "personnel" and not self.recon_dimension4_active:
                continue
            # Use i18n catalog for dimension names so they localize properly
            name = _(f"agent.recon.dimension.{dim}")
            parts.append(f"{'✅' if completed else '❌'} {name}")
        incomplete = [
            dim
            for dim, done in self.recon_dimensions_completed.items()
            if (dim != "personnel" or self.recon_dimension4_active) and not done
        ]
        status = " | ".join(parts)
        if incomplete:
            # Localize the incomplete status instruction
            status += "\n" + _("agent.recon.status_incomplete_instruction", count=len(incomplete))
        return status


class ReasoningSnapshot(BaseModel):
    """Reasoning state snapshot — stores the reasoning engine's core data.

    Responsibilities:
    - Reasoning state (reasoning)
    - Research state (research)
    - Reflexion snapshot (reflexion_snapshot)
    - Confirmed facts (confirmed_facts)
    - Unverified assumptions (unverified_assumptions)
    """

    reasoning: ReasoningState = Field(default_factory=ReasoningState)
    agent_state: AgentState = Field(
        default_factory=AgentState,
        validation_alias=AliasChoices("agent_state", "research", "board"),
    )
    reflexion_snapshot: dict[str, Any] = Field(default_factory=dict)
    confirmed_facts: list[str] = Field(
        default_factory=list, description="Facts confirmed through tool verification"
    )
    unverified_assumptions: list[str] = Field(
        default_factory=list, description="Assumptions relied on during reasoning but not yet verified"
    )

    def add_confirmed_fact(self, fact: str) -> None:
        "Add a confirmed fact (verified through tool output)."
        if fact and fact not in self.confirmed_facts:
            self.confirmed_facts.append(fact)
        if fact:
            self.reasoning.add_fact(
                key=self._fact_key_from_text(fact),
                value=fact,
                source="confirmed_fact",
                confidence=0.9,
            )

    def _fact_key_from_text(self, fact: str) -> str:
        "Infer the fact-type key from the fact text."
        text = fact.lower()
        if "cve-" in text:
            return "cve"
        if "http://" in text or "https://" in text:
            return "url"
        if "port" in text or "端口" in fact:
            return "port"
        if "server" in text or "x-powered-by" in text:
            return "service"
        if "waf" in text:
            return "waf"
        return "confirmed_fact"

    def add_assumption(self, assumption: str) -> None:
        "Add an unverified assumption."
        if assumption and assumption not in self.unverified_assumptions:
            self.unverified_assumptions.append(assumption)

    @property
    def research(self) -> AgentState:
        """Backward-compatible alias for old serialized snapshot names."""

        return self.agent_state

    @research.setter
    def research(self, value: AgentState | dict[str, Any]) -> None:
        self.agent_state = value if isinstance(value, AgentState) else AgentState.model_validate(value)


class ConstraintManager(BaseModel):
    """Constraint management — tracks constraint-violation events.

    Responsibilities:
    - Constraint-violation message list (constraint_violations)
    - Structured constraint-violation events (constraint_violation_events)
    """

    constraint_violations: list[str] = Field(default_factory=list)
    constraint_violation_events: list[ConstraintViolationEvent] = Field(
        default_factory=list
    )

    def add_constraint_violation(self, message: str) -> None:
        "Record a constraint-violation audit event."
        if not message:
            return
        if message not in self.constraint_violations:
            self.constraint_violations.append(message)
        elif self.constraint_violations and self.constraint_violations[-1] != message:
            self.constraint_violations.append(message)
        # Keep the most recent 20
        self.constraint_violations = self.constraint_violations[-20:]

    def add_constraint_violation_event(
        self,
        *,
        source: str,
        action: str = "",
        tool_name: str = "",
        code: str = "",
        severity: str = "medium",
        summary: str,
        detail: str = "",
        phase: str = "",
    ) -> None:
        "Record a structured constraint-violation audit event."
        event = ConstraintViolationEvent(
            source=source,
            action=action,
            tool_name=tool_name,
            code=code,
            severity=severity,
            phase=phase,
            summary=summary,
            detail=detail or summary,
        )
        self.constraint_violation_events.append(event)
        self.constraint_violation_events = self.constraint_violation_events[-20:]
        self.add_constraint_violation(summary)


class ExecutionHistory(BaseModel):
    """Execution history — records the pentest's executed steps and notes.

    [P18 refactor] Uses step_records as the primary record format:
    - step_records: structured step records (primary data source)
    - executed_steps: @property compatibility layer derived from step_records
    - notes: session notes

    Modified by: Nyaecho
    Modified: 2026-07-08
    Reason: unify three parallel state-tracking systems and remove data redundancy
    Note: executed_steps is now a read-only property; all writes should go through add_step()
    """

    # [P18 change] Remove the executed_steps field, replace with a @property
    step_records: list[StepRecord] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @property
    def executed_steps(self) -> list[str]:
        """[P18 compatibility layer] Generate the raw string list from step_records.

        Backward compatible with all consumers (prompt building, report generation, persistence, etc.).
        Generated dynamically on each access to ensure data consistency.
        """
        return [r.to_legacy_string() for r in self.step_records]

    def add_step(
        self,
        step: str,
        action: str = "",
        target: str = "",
        result: str = "",
        status: StepStatus = StepStatus.INFO,
        detail: str = "",
        phase: PentestPhase = PentestPhase.IDLE,
    ) -> None:
        """Record an executed step.

        [P18 change] Only writes to step_records, no longer to executed_steps.
        executed_steps is generated dynamically from step_records via @property.

        Args:
            step: raw step string (backward compatible)
            action: short action description
            target: action target
            result: result summary
            status: execution status
            detail: detailed information
            phase: current phase
        """
        # Keep the raw step (backward compatible); dedup consecutive entries to avoid title spam
        if not self.executed_steps or self.executed_steps[-1] != step:
            self.executed_steps.append(step)

        # Create a structured record
        if action:
            record = StepRecord(
                phase=phase,
                round=len(self.executed_steps),
                action=action,
                target=target,
                result=result or step[:60],
                status=status,
                detail=detail,
            )
            self.step_records.append(record)
        self._notify_checkpoint("step_complete")

    def add_note(self, note: str) -> None:
        "Add a session note, filtering out code/symbol noise."
        # Reject notes that are mostly code/symbols — they pollute evidence extraction
        chinese = re.findall(r"[\u4e00-\u9fff]", note)
        code_symbols = re.findall(
            r"[{}()=+*/<>\-\\[\\]|;|import |def |return |print\(|requests\.|socket\.|re\.|sys\.]",
            note,
        )
        if len(note) > 20 and len(code_symbols) > len(chinese) * 0.5:
            return
        # Reject very short notes
        if len(note) < 5 or note in ("---", "**", ">>>", "..."):
            return
        self.notes.append(note)

    def get_step_summary(self) -> dict[str, Any]:
        """Generate an attack-path summary.

        [P18 change] Removed the fallback logic; uses only step_records.
        executed_steps is now a @property derived from step_records.
        """
        if self.step_records:
            return self._build_step_summary_from_records()
        return {"total_steps": 0, "phases": {}, "key_findings": []}

    def _build_step_summary_from_records(self) -> dict[str, Any]:
        "Build a summary from the structured step_records."
        phases: dict[str, list[StepRecord]] = {}
        for record in self.step_records:
            phase_id = record.phase.value
            if phase_id not in phases:
                phases[phase_id] = []
            phases[phase_id].append(record)

        phase_summaries = {}
        for phase_id, records in phases.items():
            phase_summaries[phase_id] = {
                "display": phase_display_name(phase_id),
                "count": len(records),
                "actions": list(set(r.action for r in records)),
                "success_count": len([r for r in records if r.status == StepStatus.SUCCESS]),
                "failure_count": len([r for r in records if r.status == StepStatus.FAILURE]),
                "key_results": [r.to_brief() for r in records if r.status == StepStatus.SUCCESS][
                    :5
                ],
            }

        key_findings = [
            r.to_brief() for r in self.step_records if r.status == StepStatus.SUCCESS and r.result
        ][:10]

        return {
            "total_steps": len(self.step_records),
            "phases": phase_summaries,
            "key_findings": key_findings,
        }




# ==============================================================================
# [P17 refactor end] Sub-state class definitions
# ==============================================================================


# ==============================================================================
# [P17 refactor] SessionState refactored using composition
# Modified by: Nyaecho
# Modified: 2026-07-08
# Reason: SessionState originally had 22 fields, violating the single-responsibility principle
#          adopt composition, delegating responsibilities to 6 sub-state classes
# Note: keep @property proxies for all original fields to ensure backward compatibility
#          sub-state instances are PrivateAttr and do not affect serialization
#          save()/load() are unchanged; the JSON format stays compatible
# ==============================================================================

class SessionState(BaseModel):
    """Full session state for a pentest engagement.

    [P17 refactor] Uses composition, internally backed by 6 sub-state classes:
    - SessionConfig: session configuration
    - VulnerabilityStore: finding management
    - ReconState: recon state
    - ReasoningSnapshot: reasoning state
    - ConstraintManager: constraint management
    - ExecutionHistory: execution history

    All original fields keep backward compatibility through @property proxies.
    """

    # ★ Sub-state instances (PrivateAttr, do not affect serialization)
    _config: SessionConfig = PrivateAttr(default_factory=SessionConfig)
    _vulnerabilities: VulnerabilityStore = PrivateAttr(default_factory=VulnerabilityStore)
    _recon: ReconState = PrivateAttr(default_factory=ReconState)
    _reasoning_snapshot: ReasoningSnapshot = PrivateAttr(default_factory=ReasoningSnapshot)
    _constraints: ConstraintManager = PrivateAttr(default_factory=ConstraintManager)
    _history: ExecutionHistory = PrivateAttr(default_factory=ExecutionHistory)

    # ★ Original fields kept for serialization compatibility; actual values live in the sub-states
    # Note: these fields are serialized on model_dump(), but reads/writes go through @property proxies

    def model_post_init(self, __context: Any) -> None:
        "After initialization, sync field values to the sub-states."
        # Restore sub-states from serialized data
        self._config = SessionConfig(
            target=self.target,
            phase=self.phase,
            started_at=self.started_at,
            resume_summary=self.resume_summary,
            resume_meta=self.resume_meta,
            task_constraints=self.task_constraints,
        )
        self._vulnerabilities = VulnerabilityStore(
            target=self.target,
            findings=self.findings,
            semantic_dedup_threshold=self.semantic_dedup_threshold,
        )
        self._recon = ReconState(
            recon_data=self.recon_data,
            recon_dimensions_completed=self.recon_dimensions_completed,
            recon_dimension4_active=self.recon_dimension4_active,
        )
        self._reasoning_snapshot = ReasoningSnapshot(
            reasoning=self.reasoning,
            agent_state=self.agent_state,
            reflexion_snapshot=self.reflexion_snapshot,
            confirmed_facts=self.confirmed_facts,
            unverified_assumptions=self.unverified_assumptions,
        )
        self._constraints = ConstraintManager(
            constraint_violations=self.constraint_violations,
            constraint_violation_events=self.constraint_violation_events,
        )
        self._history = ExecutionHistory(
            step_records=self.step_records,
            notes=self.notes,
        )

    # ==========================================================================
    # Field definitions (for serialization compatibility)
    # ==========================================================================

    target: Optional[str] = None
    phase: PentestPhase = PentestPhase.IDLE
    started_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    resume_summary: str = Field(default="", description="Historical-results summary injected on resume")
    resume_meta: dict[str, Any] = Field(default_factory=dict, description="Resume metadata")
    task_constraints: TaskConstraints = Field(default_factory=TaskConstraints)
    constraint_violations: list[str] = Field(default_factory=list)
    constraint_violation_events: list[ConstraintViolationEvent] = Field(default_factory=list)
    reasoning: ReasoningState = Field(default_factory=ReasoningState)
    agent_state: AgentState = Field(
        default_factory=AgentState,
        validation_alias=AliasChoices("agent_state", "research", "board"),
    )
    reflexion_snapshot: dict[str, Any] = Field(default_factory=dict)
    findings: list[VulnerabilityFinding] = Field(default_factory=list)
    recon_data: dict[str, Any] = Field(default_factory=dict)
    # [P18 change] executed_steps is now a @property derived from step_records
    # No longer a field; generated dynamically via @property
    step_records: list[StepRecord] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    confirmed_facts: list[str] = Field(default_factory=list, description="Facts confirmed through tool verification")
    unverified_assumptions: list[str] = Field(
        default_factory=list, description="Assumptions relied on during reasoning but not yet verified"
    )
    recon_dimensions_completed: dict[str, bool] = Field(
        default_factory=lambda: {
            "server": False,
            "website": False,
            "domain": False,
            "personnel": False,
        },
        description="Four-dimension information-gathering model completion tracking",
    )
    recon_dimension4_active: bool = Field(default=False, description="Whether dimension four (personnel info) is activated")
    # ★ Active skill selection for this turn/child task — structured provenance
    # source. Stored as a plain dict to avoid importing the resolver here.
    active_skill_selection: Optional[dict[str, Any]] = Field(
        default=None, description="Active SkillSelection.to_provenance() for the current turn"
    )
    # ★ Run events emitted whenever the active skill selection changes.
    skill_selection_events: list[dict[str, Any]] = Field(
        default_factory=list, description="Audit log of skill-selection changes"
    )
    subagent_events: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Bounded durable projection of sub-agent runtime events",
    )
    subagent_evidence_provenance: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Parent evidence id to originating sub-agent task identity",
    )
    semantic_dedup_threshold: float = Field(
        default=0.75, description="Similarity threshold for semantic dedup (0-1)"
    )
    session_kind: str = Field(
        default="parent", description="Session owner kind: parent, group_leader, or leaf"
    )
    run_id: str = Field(default="", description="Owning solve/runtime identifier")
    parent_session_id: str = Field(
        default="", description="Parent session identifier for sub-agent checkpoints"
    )
    task_id: str = Field(default="", description="Sub-agent task identifier")
    lifecycle_status: str = Field(
        default="", description="Last persisted sub-agent lifecycle status"
    )

    # ★ Finding dedup tracking (PrivateAttr)
    _finding_ids_cache: set[str] = PrivateAttr(default_factory=set)
    _content_hash: str = PrivateAttr(default="")
    _save_path: Optional[Path] = PrivateAttr(default=None)
    _checkpoint_transform: Callable[
        ["SessionState", dict[str, Any]], dict[str, Any]
    ] | None = PrivateAttr(default=None)
    _checkpoint_callback: Callable[["SessionState", str], None] | None = PrivateAttr(
        default=None
    )

    def set_checkpoint_callback(
        self, callback: Callable[["SessionState", str], None] | None
    ) -> None:
        """Install a persistence callback fired at durable state boundaries."""
        self._checkpoint_callback = callback

    def _notify_checkpoint(self, reason: str) -> None:
        if self._checkpoint_callback is None:
            return
        self._checkpoint_callback(self, reason)

    @property
    def research(self) -> AgentState:
        """Compatibility alias for pre-AgentState integrations."""

        return self.agent_state

    @research.setter
    def research(self, value: AgentState | dict[str, Any]) -> None:
        self.agent_state = value if isinstance(value, AgentState) else AgentState.model_validate(value)
        self._reasoning_snapshot.agent_state = self.agent_state

    # ==========================================================================
    # @property proxies (keep backward compatibility)
    # ==========================================================================

    @property
    def executed_steps(self) -> list[str]:
        """[P18 compatibility layer] Generate the raw string list from step_records.

        Backward compatible with all consumers (prompt building, report generation, persistence, etc.).
        Generated dynamically on each access to ensure data consistency.
        """
        return [r.to_legacy_string() for r in self.step_records]

    @executed_steps.setter
    def executed_steps(self, value: list[str]) -> None:
        """[P18 compatibility layer] Allow setting executed_steps (backward compatible).

        Converts the old-format string list into step_records.
        """
        self.step_records = [
            StepRecord.from_legacy_string(s, self.phase) for s in value
        ]
        # Sync to the sub-state
        self._history.step_records = self.step_records

    # Note: the other fields are already directly accessible
    # Sub-state class methods are invoked through delegation methods

    # ==========================================================================
    # Delegation methods (delegate to the sub-state classes)
    # ==========================================================================

    def add_finding(self, finding: VulnerabilityFinding) -> bool:
        """Add a finding with automatic dedup (the single place that implements adding/deduping).

        Dedup strategy:
        1. exact finding_id hash match (fast)
        2. semantic-similarity match (captures different phrasings of the same finding); on a hit, keep the one with stronger evidence

        Writes to self.findings / self._finding_ids_cache and syncs the same reference to
        VulnerabilityStore (the read-only query view). A successful add or replace triggers a checkpoint,
        making "finding a vulnerability" a persistable progress boundary.
        """
        # Generate a finding_id (if not already set)
        if hasattr(finding, "_sync_status_fields"):
            finding._sync_status_fields()
        if not finding.finding_id:
            finding.finding_id = finding._generate_finding_id()

        # Tie the finding to the owning target when the caller didn't set one.
        if not finding.target and self.target:
            finding.target = self.target

        # Layer 1: exact finding_id dedup
        if finding.finding_id in self._finding_ids_cache:
            logger.debug(_rl("跳过重复漏洞: %s (ID: %s)", "Skipping duplicate finding: %s (ID: %s)"), finding.title, finding.finding_id)
            return False

        # Layer 2: semantic-similarity dedup
        from vulnclaw.agent.finding_similarity import (
            _evidence_strength,
            finding_similarity,
        )

        for idx, existing in enumerate(self.findings):
            if finding_similarity(finding, existing) >= self.semantic_dedup_threshold:
                # Semantic duplicate hit: keep the one with stronger evidence
                if _evidence_strength(finding) > _evidence_strength(existing):
                    logger.debug(
                        _rl("语义重复，替换为证据更强的漏洞: %s 取代 %s", "Semantic duplicate; replaced by a stronger-evidence finding: %s supersedes %s"),
                        finding.title,
                        existing.title,
                    )
                    self._finding_ids_cache.discard(existing.finding_id)
                    self._finding_ids_cache.add(finding.finding_id)
                    self.findings[idx] = finding
                    self._notify_checkpoint("finding_updated")
                else:
                    logger.debug(_rl("跳过语义重复漏洞: %s", "Skipping semantically duplicate finding: %s"), finding.title)
                return False

        # Attach skill provenance (when not explicitly provided and a selection is active). Deep-copy so its
        # references_loaded list is not shared with active_skill_selection — otherwise a later
        # record_loaded_reference() would retroactively modify the provenance of already-recorded findings.
        if finding.skill_provenance is None and self.active_skill_selection is not None:
            finding.skill_provenance = copy.deepcopy(self.active_skill_selection)

        # Add to the tracking set and list
        self._finding_ids_cache.add(finding.finding_id)
        self.findings.append(finding)

        # Sync to the sub-state
        self._vulnerabilities.findings = self.findings
        self._vulnerabilities._finding_ids_cache = self._finding_ids_cache

        self._notify_checkpoint("finding_added")
        return True

    def get_verified_findings(self) -> list[VulnerabilityFinding]:
        "Get the verified findings, delegating to VulnerabilityStore."
        return self._vulnerabilities.get_verified_findings()

    def get_rejected_findings(self) -> list[VulnerabilityFinding]:
        "Get the rejected findings, delegating to VulnerabilityStore."
        return self._vulnerabilities.get_rejected_findings()

    def get_pending_findings(self) -> list[VulnerabilityFinding]:
        "Get the pending findings, delegating to VulnerabilityStore."
        return self._vulnerabilities.get_pending_findings()

    def get_candidate_findings(self) -> list[VulnerabilityFinding]:
        "Get the candidate findings, delegating to VulnerabilityStore."
        return self._vulnerabilities.get_candidate_findings()

    def get_pending_verification_findings(self) -> list[VulnerabilityFinding]:
        "Get the findings awaiting verification, delegating to VulnerabilityStore."
        return self._vulnerabilities.get_pending_verification_findings()

    def get_manual_review_findings(self) -> list[VulnerabilityFinding]:
        "Get the findings needing manual review, delegating to VulnerabilityStore."
        return self._vulnerabilities.get_manual_review_findings()

    def add_recon_subdomain(self, subdomain: str) -> None:
        """Record a discovered subdomain.

        [P17 refactor] Also updates self.recon_data for backward compatibility.
        """
        if "subdomains" not in self.recon_data:
            self.recon_data["subdomains"] = []
        if subdomain and subdomain not in self.recon_data["subdomains"]:
            self.recon_data["subdomains"].append(subdomain)
        # Sync to the sub-state
        self._recon.recon_data = self.recon_data

    def mark_recon_dimension(self, dimension: str) -> None:
        """Mark a recon dimension as completed.

        [P17 refactor] Also updates self.recon_dimensions_completed for backward compatibility.
        """
        if dimension in self.recon_dimensions_completed:
            self.recon_dimensions_completed[dimension] = True
            # Sync to the sub-state
            self._recon.recon_dimensions_completed = self.recon_dimensions_completed

    def is_recon_complete(self) -> bool:
        "Check whether recon is complete, delegating to ReconState."
        return self._recon.is_recon_complete()

    def get_recon_status_text(self) -> str:
        "Get the recon status text, delegating to ReconState."
        return self._recon.get_recon_status_text()

    def add_constraint_violation(self, message: str) -> None:
        """Record a constraint violation.

        [P17 refactor] Also updates self.constraint_violations for backward compatibility.
        """
        if not message:
            return
        if message not in self.constraint_violations:
            self.constraint_violations.append(message)
        elif self.constraint_violations and self.constraint_violations[-1] != message:
            self.constraint_violations.append(message)
        # Keep the most recent 20
        self.constraint_violations = self.constraint_violations[-20:]
        # Sync to the sub-state
        self._constraints.constraint_violations = self.constraint_violations

    def add_constraint_violation_event(
        self,
        *,
        source: str,
        action: str = "",
        tool_name: str = "",
        code: str = "",
        severity: str = "medium",
        summary: str,
        detail: str = "",
    ) -> None:
        """Record a structured constraint-violation event.

        [P17 refactor] Also updates self.constraint_violation_events for backward compatibility.
        """
        phase_str = self.phase.value if hasattr(self.phase, "value") else str(self.phase)
        event = ConstraintViolationEvent(
            source=source,
            action=action,
            tool_name=tool_name,
            code=code,
            severity=severity,
            phase=phase_str,
            summary=summary,
            detail=detail or summary,
        )
        self.constraint_violation_events.append(event)
        self.constraint_violation_events = self.constraint_violation_events[-20:]
        self.add_constraint_violation(summary)
        # Sync to the sub-state
        self._constraints.constraint_violation_events = self.constraint_violation_events

    def add_step(
        self,
        step: str,
        action: str = "",
        target: str = "",
        result: str = "",
        status: StepStatus = StepStatus.INFO,
        detail: str = "",
    ) -> None:
        """Record an executed step.

        [P18 change] Only writes to step_records, no longer to executed_steps.
        executed_steps is now a @property generated dynamically from step_records.
        """
        # [P18 change] Always create a structured record, using step as the default for action
        record = StepRecord(
            phase=self.phase,
            round=len(self.step_records) + 1,
            action=action or step[:60],
            target=target,
            result=result or step[:60],
            status=status,
            detail=detail,
        )
        self.step_records.append(record)
        # Sync to the sub-state
        self._history.step_records = self.step_records

    def get_step_summary(self) -> dict[str, Any]:
        "Generate an attack-path summary, delegating to ExecutionHistory."
        return self._history.get_step_summary()

    def add_note(self, note: str) -> None:
        """Add a session note.

        [P17 refactor] Also updates self.notes for backward compatibility.
        """
        # Reject notes that are mostly code/symbols
        chinese = re.findall(r"[\u4e00-\u9fff]", note)
        code_symbols = re.findall(
            r"[{}()=+*/<>\-\\[\\]|;|import |def |return |print\(|requests\.|socket\.|re\.|sys\.]",
            note,
        )
        if len(note) > 20 and len(code_symbols) > len(chinese) * 0.5:
            return
        # Reject very short notes
        if len(note) < 5 or note in ("---", "**", ">>>", "..."):
            return
        self.notes.append(note)
        # Sync to the sub-state
        self._history.notes = self.notes

    def set_active_skill_selection(self, provenance: Optional[dict[str, Any]]) -> bool:
        """Record the active skill selection; emit a run event when it changes.

        Args:
            provenance: A ``SkillSelection.to_provenance()`` dict (or None).

        Returns:
            True if the selection changed from the previous turn.
        """
        prev = self.active_skill_selection
        changed = (prev or {}).get("primary") != (provenance or {}).get("primary") or (
            (prev or {}).get("supporting") != (provenance or {}).get("supporting")
        )
        # Same bundle as last turn: carry over references already loaded under it
        # so provenance keeps a complete record across turns.
        if not changed and prev is not None and provenance is not None:
            loaded = prev.get("references_loaded")
            if loaded and not provenance.get("references_loaded"):
                provenance = {**provenance, "references_loaded": list(loaded)}
        self.active_skill_selection = provenance
        if changed:
            event = {
                "kind": "skill_selection_changed" if provenance is not None else "skill_selection_cleared",
                "timestamp": datetime.now().isoformat(),
                "primary": (provenance or {}).get("primary"),
                "supporting": (provenance or {}).get("supporting", []),
                "reason": (provenance or {}).get("reason", ""),
                "confidence": (provenance or {}).get("confidence", 0.0),
            }
            self.skill_selection_events.append(event)
            self.skill_selection_events = self.skill_selection_events[-50:]
        self._notify_checkpoint("skill_selection_changed")
        return changed

    def record_loaded_reference(self, skill_name: str, ref_name: str) -> None:
        """Track a reference loaded under the current skill selection."""
        if self.active_skill_selection is None:
            return
        entry = f"{skill_name}/{ref_name}" if skill_name else ref_name
        loaded = self.active_skill_selection.setdefault("references_loaded", [])
        if entry and entry not in loaded:
            loaded.append(entry)

    def add_confirmed_fact(self, fact: str) -> None:
        """Add a confirmed fact.

        [P17 refactor] Also updates self.confirmed_facts and self.reasoning
        for backward compatibility.
        """
        if fact and fact not in self.confirmed_facts:
            self.confirmed_facts.append(fact)
        if fact:
            self.reasoning.add_fact(
                key=self._fact_key_from_text(fact),
                value=fact,
                source="confirmed_fact",
                confidence=0.9,
            )
        # Sync to the sub-state
        self._reasoning_snapshot.confirmed_facts = self.confirmed_facts
        self._reasoning_snapshot.reasoning = self.reasoning

    def _fact_key_from_text(self, fact: str) -> str:
        "Infer the fact-type key from the fact text."
        text = fact.lower()
        if "cve-" in text:
            return "cve"
        if "http://" in text or "https://" in text:
            return "url"
        if "port" in text or "端口" in fact:
            return "port"
        if "server" in text or "x-powered-by" in text:
            return "service"
        if "waf" in text:
            return "waf"
        return "confirmed_fact"

    def add_assumption(self, assumption: str) -> None:
        "Add an unverified assumption."
        if assumption and assumption not in self.unverified_assumptions:
            self.unverified_assumptions.append(assumption)
        # Sync to the sub-state
        self._reasoning_snapshot.unverified_assumptions = self.unverified_assumptions

    def get_constraints_prompt_block(self) -> str:
        "Get the constraint prompt block, delegating to TaskConstraints."
        return self.task_constraints.to_prompt_block()

    def advance_phase(self, phase: PentestPhase) -> None:
        "Switch to a new phase."

        old_phase = self.phase
        self.phase = phase
        old_display = phase_display_name(old_phase)
        new_display = phase_display_name(phase)
        # Record the phase switch
        self.add_step(
            step=_("step.phase_transition", phase=new_display),
            action=_("step.phase_transition.action"),
            target=f"{old_display} → {new_display}",
            result=_("step.phase_transition.result", phase=new_display),
            status=StepStatus.INFO,
        )
        self._notify_checkpoint("phase_transition")

    def save(self, path: Optional[Path] = None) -> Path:
        """Save the session state to a JSON file.

        [P18 change] Ensures executed_steps is serialized into the JSON
        for backward compatibility.
        [Perf] Compares an MD5 content hash to skip unchanged writes.
        """
        if path is None and self._save_path is not None:
            path = self._save_path
        if path is None:
            from vulnclaw.config.settings import SESSIONS_DIR

            safe_target = (self.target or "unknown").replace("/", "_").replace(":", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = SESSIONS_DIR / f"{timestamp}_{safe_target}.json"
        else:
            path = Path(path)
        self._save_path = path

        path.parent.mkdir(parents=True, exist_ok=True)
        # [P18 compat] Get the serialized data and add executed_steps
        data = self.model_dump(mode="json")
        if self._checkpoint_transform is not None:
            data = self._checkpoint_transform(self, data)
        data["executed_steps"] = self.executed_steps
        content = json.dumps(data, ensure_ascii=False, indent=2)

        content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
        if content_hash == self._content_hash:
            return path
        self._content_hash = content_hash

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def set_save_path(self, path: Path) -> None:
        """Pin future no-argument saves to one collision-free checkpoint."""

        self._save_path = Path(path)

    @classmethod
    def load(cls, path: Path) -> "SessionState":
        """Load the session state from a JSON file.

        [P18 change] Handles the old JSON format (with an executed_steps field)
        and converts it into the step_records format.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # [P18 compat] If only executed_steps is present, convert it to step_records
        if "executed_steps" in data and "step_records" not in data:
            data["step_records"] = [
                StepRecord.from_legacy_string(s) for s in data["executed_steps"]
            ]

        # [P18 compat] Remove the executed_steps field to avoid a Pydantic validation error
        data.pop("executed_steps", None)

        state = cls(**data)
        state.set_save_path(path)
        return state

# ==============================================================================
# [P17 refactor end] SessionState composition refactor
# ==============================================================================


class ContextManager:
    """Manages conversation context and session state."""

    def __init__(
        self,
        max_history: int = 200,
        memory_store: Any = None,
        *,
        max_tokens: int = 32000,
        search_max_chars: int = 6000,
    ) -> None:
        self.max_history = max(1, int(max_history))
        self.max_tokens = max(256, int(max_tokens))
        self.search_max_chars = max(256, int(search_max_chars))
        self.messages: list[dict[str, Any]] = []
        self.state = SessionState()
        self.memory_store = memory_store
        # Context Vault: selective, model-driven archiving layered on top of the
        # deterministic compactor.  Initialized lazily so tool dispatch and the
        # budget pipeline can attach it without import cycles.
        self.vault: Any = None
        self.vault_output_dir: Path | None = None

    def ensure_vault(self) -> Any:
        """Lazily create the vault manager for this session."""
        if self.vault is None:
            from vulnclaw.agent.context_vault import VaultConfig, VaultManager

            self.vault = VaultManager(
                output_dir=self.vault_output_dir,
                config=VaultConfig(),
            )
        return self.vault

    def attach_vault(self, vault: Any, output_dir: Path | None = None) -> None:
        """Attach an externally-created vault (used by tests and CLI wiring)."""
        self.vault = vault
        if output_dir is not None:
            self.vault_output_dir = output_dir
            setter = getattr(vault, "set_output_dir", None)
            if callable(setter):
                setter(output_dir)

    def add_user_message(self, content: str) -> None:
        """Add a user message to context."""
        self.messages.append({"role": "user", "content": content})
        self._trim()

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to context."""
        self.messages.append({"role": "assistant", "content": content})
        self._trim()

    def add_message(self, message: dict[str, Any]) -> None:
        """Add a raw chat message to context.

        Tool-call transcripts need fields such as ``tool_calls`` and
        ``tool_call_id``.  Keeping the original Chat Completions message shape
        lets later model turns see the same cause/effect structure that produced
        the evidence, instead of only a lossy text summary.
        """
        if not isinstance(message, dict):
            return
        role = str(message.get("role", "") or "").strip()
        if not role:
            return
        stored_message = copy.deepcopy(message)
        if role == "tool":
            stored_message = self._offload_large_tool_message(stored_message)
        self.messages.append(stored_message)
        self._trim()

    def add_system_message(self, content: str) -> None:
        """Add a system message (inserted at beginning)."""
        # System messages are handled separately in the API call
        pass

    def get_messages(self) -> list[dict[str, Any]]:
        """Get conversation messages for API call."""
        return copy.deepcopy(self.messages)

    def reset(self) -> None:
        """Reset context and session state."""
        self.messages = []
        self.state = SessionState()
        if self.memory_store is not None:
            new_scope = getattr(self.memory_store, "new_scope", None)
            if callable(new_scope):
                new_scope()

    def _memory_scope(self) -> str:
        return str(getattr(self.memory_store, "session_id", "") or "")

    def _archive_messages(self, messages: list[dict[str, Any]], *, kind: str) -> str:
        if not messages or self.memory_store is None:
            return ""
        try:
            return str(
                self.memory_store.archive_messages(
                    copy.deepcopy(messages),
                    scope=self._memory_scope(),
                    target=str(self.state.target or ""),
                    kind=kind,
                )
                or ""
            )
        except (OSError, ValueError, TypeError) as exc:
            logger.warning("Cold-memory archive failed; retaining hot history: %s", exc)
            return ""

    def _offload_large_tool_message(self, message: dict[str, Any]) -> dict[str, Any]:
        from vulnclaw.agent.token_counter import estimate_message_tokens

        if self.memory_store is None or estimate_message_tokens(message) <= self.max_tokens // 2:
            return message
        record_id = self._archive_messages([message], kind="large_tool_result")
        if not record_id:
            return message
        content = str(message.get("content", "") or "")
        preview = content[:2000]
        if len(content) > len(preview):
            preview += "..."
        message["content"] = (
            f"[cold-memory:{record_id}] Large tool result archived. "
            f"Use memory_search with query '{record_id}' for a bounded excerpt.\n{preview}"
        )
        return message

    def _over_hot_limit(self, messages: list[dict[str, Any]]) -> bool:
        from vulnclaw.agent.token_counter import estimate_tokens

        return len(messages) > self.max_history or estimate_tokens(messages) > self.max_tokens

    def _trim(self) -> None:
        """Spill old messages to cold memory at the hot-history cap.

        Normal request-time compaction is driven by the token budget manager.
        This remains a safety net for callers that keep adding messages without
        issuing an LLM request.
        """
        if not self._over_hot_limit(self.messages):
            return

        from vulnclaw.agent.token_counter import group_conversation_turns, group_tool_exchanges

        candidate = list(self.messages)
        turns = group_conversation_turns(candidate)
        archived_messages: list[dict[str, Any]] = []
        while self._over_hot_limit(candidate) and len(turns) > 1:
            archived = turns.pop(0)
            archived_messages.extend(archived)
            candidate = candidate[len(archived) :]

        # A single automated subtask can itself contain hundreds of tool
        # exchanges. Keep its user instruction as a hot anchor, then spill the
        # oldest complete exchanges until the window is bounded.
        exchanges = group_tool_exchanges(candidate)
        while self._over_hot_limit(candidate) and len(exchanges) > 2:
            remove_at = 1 if exchanges[0][0].get("role") == "user" else 0
            archived = exchanges.pop(remove_at)
            archived_messages.extend(archived)
            candidate = [message for exchange in exchanges for message in exchange]

        if not archived_messages:
            return
        if self.memory_store is not None and not self._archive_messages(
            archived_messages, kind="history"
        ):
            return
        self.messages = candidate

    def search_cold_memory(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        """Retrieve relevant archived turns only when explicitly requested."""
        if self.memory_store is None:
            return []
        return self.memory_store.search_messages(
            query,
            limit=limit,
            max_chars=self.search_max_chars,
            scope=self._memory_scope(),
            target=str(self.state.target or ""),
        )

    @staticmethod
    def _is_context_digest_message(message: dict[str, Any]) -> bool:
        content = str(message.get("content", "") or "")
        return message.get("role") == "system" and content.startswith("[context digest")

    def replace_history_with_digest(
        self,
        digest_message: dict[str, Any],
        recent_messages: list[dict[str, Any]],
    ) -> None:
        """Atomically replace older history with a prompt-safe context digest."""
        cleaned_recent = [
            copy.deepcopy(message)
            for message in recent_messages
            if isinstance(message, dict) and not self._is_context_digest_message(message)
        ]
        self.messages = [copy.deepcopy(digest_message), *cleaned_recent]

    def compact_messages(self, *, max_recent: int = 24, note: str = "") -> str:
        """Compact older conversation message groups for `/compact` or safety fallback."""
        from vulnclaw.agent.token_counter import group_messages

        groups = group_messages(self.messages)
        if len(groups) <= max_recent:
            return "No compaction needed."

        recent_groups: list[list[dict[str, Any]]] = []
        recent_count = 0
        while groups and recent_count < max_recent:
            group = groups.pop()
            recent_groups.insert(0, group)
            recent_count += len(group)
        recent = [message for group in recent_groups for message in group]
        old = [message for group in groups for message in group]
        summary = self._compress_messages(old) or "(older conversation omitted)"
        if note:
            summary = f"{note}\n{summary}"
        digest = {"role": "system", "content": f"[context digest v1]\n{summary}"}
        self.replace_history_with_digest(digest, recent)
        agent_state = getattr(self.state, "agent_state", None)
        if agent_state is not None:
            evidence_ids = [item.id for item in getattr(agent_state, "evidence", [])[-12:]]
            if hasattr(agent_state, "update_context_digest"):
                agent_state.update_context_digest(summary, evidence_ids)
            else:
                agent_state.compact_summary = summary
        return summary

    @staticmethod
    def _compress_messages(messages: list[dict[str, Any]]) -> str:
        """Compress a list of messages into a concise summary.

        Extracts key findings, tool results, and discoveries from the
        conversation history so the LLM doesn't completely lose context.
        """
        key_parts = []

        for msg in messages:
            content = msg.get("content", "")
            # Extract tool call/result information — these contain actual findings
            if "调用工具:" in content or "工具结果:" in content:
                key_parts.append(content[:300])

            # Extract lines that look like findings/discoveries
            for line in content.split("\n"):
                stripped = line.strip()
                if any(
                    marker in stripped
                    for marker in [
                        "[+]",
                        "[!]",
                        "[-]",
                        "发现",
                        "漏洞",
                        "flag",
                        "CVE",
                        "端口",
                        "开放",
                        "服务",
                        "路径",
                        "泄露",
                        "注入",
                        "Status:",
                        "Headers:",
                        "Body",
                        # ★ Negative/failure markers — critical for CTF to avoid repeating
                        "失败",
                        "无效",
                        "没有",
                        "返回相同",
                        "被拦截",
                        "未成功",
                        "不存在",
                        "错误",
                        "404",
                        "timeout",
                        # ★ Confirmed fact markers — verified by actual tool output
                        "已确认",
                        "确认",
                        "验证成功",
                        "verified",
                        "confirmed",
                        # ★ Assumption markers — things the LLM assumed but didn't verify
                        "假设",
                        "应该",
                        "可能",
                        "推测",
                        "猜测",
                        "估计",
                    ]
                ):
                    key_parts.append(stripped[:200])

        if not key_parts:
            return ""

        # Limit total summary size to avoid context bloat
        summary = "\n".join(key_parts)
        if len(summary) > 3000:
            summary = summary[:3000] + "\n...(更多历史记录已省略)"

        return summary

    def trim_messages(self, max_messages: int = 20) -> None:
        """Forcefully trim conversation history to a specific size.

        Used when context overflow causes repeated LLM errors.
        """
        original_limit = self.max_history
        try:
            self.max_history = max(1, max_messages)
            self._trim()
        finally:
            self.max_history = original_limit
