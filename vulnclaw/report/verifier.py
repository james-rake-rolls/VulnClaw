"""VulnClaw Vulnerability Verifier — validate findings before they enter the report.

Core principle: an unverified vulnerability = a false positive = not written to the report

Workflow:
    1. Receive a vulnerability hypothesis (pending finding)
    2. Generate PoC code
    3. Execute the PoC via python_execute
    4. Decide the result: verified / rejected
    5. Only verified findings may enter the report
"""

from __future__ import annotations

import logging
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Modified by: Nyaecho
# Modified: 2026-07-08
# Reason: eliminate a V2 violation — leaf types moved to config/domain_models.py.
from vulnclaw.config.domain_models import VulnerabilityFinding
from vulnclaw.i18n import bi as _rl

logger = logging.getLogger(__name__)


class VerificationStatus(str, Enum):
    "Vulnerability verification status."

    PENDING = "pending"  # Pending verification
    VERIFIED = "verified"  # Verified
    REJECTED = "rejected"  # Verification failed / false positive
    SKIPPED = "skipped"  # Verification skipped (e.g. an already-confirmed fact)


class VerificationResult(str, Enum):
    "Verification-result details."

    # Verified outcomes
    VULN_CONFIRMED = "vuln_confirmed"  # Vulnerability confirmed
    SENSITIVE_DATA_EXPOSED = "sensitive_data"  # Sensitive data exposure
    SECURITY_BYPASS = "security_bypass"  # Security-control bypass

    # Rejected outcomes
    FALSE_POSITIVE = "false_positive"  # False positive
    NO_RESPONSE_DIFF = "no_response_diff"  # No response difference
    PARAM_INVALID = "param_invalid"  # Invalid parameter
    NORMAL_RESPONSE = "normal_response"  # Normal response
    TIMEOUT = "timeout"  # Timeout
    ERROR_403_404 = "error_403_404"  # 403/404 normal rejection
    EXECUTION_ERROR = "execution_error"  # PoC execution-environment error (e.g. missing interpreter)
    APPROVAL_REQUIRED = "approval_required"  # Execution not approved; PoC did not run


@dataclass
class VerifiedFinding:
    "A verified finding."

    # Information from the original finding
    original_finding: VulnerabilityFinding

    # Verification status
    status: VerificationStatus = VerificationStatus.PENDING
    result: Optional[VerificationResult] = None

    # PoC information
    poc_code: Optional[str] = None
    poc_output: Optional[str] = None
    poc_executed_at: Optional[str] = None

    # Verification conclusion
    verified_description: str = ""
    verified_evidence: str = ""
    verified_severity: str = ""  # Severity may be adjusted based on the verification result

    # Rejection reason (if verification failed)
    rejection_reason: str = ""

    # Verifier (metadata)
    verified_by: str = "verifier_module"
    verified_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ── PoC generator ────────────────────────────────────────────────────────────────


class PoCGenerator:
    "Generate PoC code from a vulnerability hypothesis."

    # Vulnerability type -> PoC template mapping
    #
    # ⚠️ The templates use *single braces* as Python syntax (dict literals, f-string interpolation).
    # The only template placeholders are ``{target}`` / ``{payload}`` / ``{baseline_len}`` /
    # ``{path}``, replaced exactly by :meth:`generate_poc` via ``str.replace``.
    # Do not use ``{{`` / ``}}`` escaping — the renderer is not ``str.format``, so double braces would remain
    # verbatim in the generated PoC, turning a ``dict`` literal into a ``set`` (``TypeError``) or
    # making an f-string print the literal ``{var}`` text instead of the interpolated result.
    POC_TEMPLATES: dict[str, str] = {
        "sql_injection": """
import requests

target = "{target}"
params = {
    "id": "{payload}",
}

try:
    r = requests.get(target, params=params, timeout=10, verify=False)
    text = r.text.lower()

    # SQL error signatures
    sql_errors = [
        "sql syntax", "mysql", "sqlite", "postgres", "oracle",
        "sqlstate", "microsoft sql", "odbc", "syntax error",
        "you have an error in your sql", "warning: mysql",
    ]

    for err in sql_errors:
        if err in text:
            print(f"[CONFIRMED] SQL injection: detected SQL error signature '{err}'")
            print(f"[INFO] Response status code: {r.status_code}")
            exit(0)

    # Check response differences (if a normal baseline is provided)
    baseline_len = {baseline_len}
    if len(r.content) != baseline_len and baseline_len > 0:
        print(f"[POSSIBLE] Abnormal response length: {len(r.content)} vs baseline {baseline_len}")

    print("[REJECTED] No SQL-injection signature detected")
except requests.Timeout:
    print("[REJECTED] Request timed out")
except Exception as e:
    print(f"[ERROR] {e}")
""",
        "xss": """
import requests

target = "{target}"
payload = "{payload}"

try:
    r = requests.get(target, params={"q": payload}, timeout=10, verify=False)

    if payload in r.text:
        print("[CONFIRMED] XSS: payload appears in the response")
        print("[INFO] XSS payload sent; verbatim reflection detected")
        exit(0)

    print("[REJECTED] XSS payload did not appear in the response")
except Exception as e:
    print(f"[ERROR] {e}")
""",
        "command_injection": """
import requests

target = "{target}"
params = {
    "cmd": "{payload}",
}

try:
    r = requests.get(target, params=params, timeout=10, verify=False)
    text = r.text

    # Command-injection signatures
    cmd_indicators = ["uid=", "gid=", "root:", "/bin/bash", "whoami", "linux"]

    for indicator in cmd_indicators:
        if indicator in text:
            print(f"[CONFIRMED] Command injection: detected '{indicator}'")
            exit(0)

    print("[REJECTED] No command-injection signature detected")
except Exception as e:
    print(f"[ERROR] {e}")
""",
        "debug_mode": """
import requests

target = "{target}"

try:
    # Normal request
    r_normal = requests.get(target, timeout=10, verify=False)
    len_normal = len(r_normal.content)

    # Debug-mode request
    r_debug = requests.get(target + "/?debug=1", timeout=10, verify=False)
    len_debug = len(r_debug.content)

    print(f"[INFO] Normal response length: {len_normal}")
    print(f"[INFO] debug=1 response length: {len_debug}")

    # Check for debug info disclosure
    if len_debug != len_normal:
        diff = len_debug - len_normal
        print(f"[POSSIBLE] Debug-mode response differs from normal, diff: {diff} bytes")

        # Check whether sensitive info is actually disclosed
        debug_content = r_debug.text.replace(r_normal.text, "")
        if debug_content:
            sensitive_keywords = ["password", "secret", "api_key", "token", "db_", "connection"]
            for kw in sensitive_keywords:
                if kw.lower() in debug_content.lower():
                    print(f"[CONFIRMED] Debug mode leaks sensitive information: detected '{kw}'")
                    exit(0)

        # If only the response length differs but no sensitive info, downgrade to Info
        print("[INFO] Debug-mode response differs but no sensitive info disclosure found; downgrading to Info")

    # Check for debug-related keywords
    if "debug" in r_debug.text.lower() and r_debug.text.lower().count("debug") > r_normal.text.lower().count("debug"):
        print("[POSSIBLE] debug mode contains extra debug info")

    print("[REJECTED] Debug mode: no obvious sensitive-info disclosure found")

except Exception as e:
    print(f"[ERROR] {e}")
""",
        "lfi": """
import requests

target = "{target}"
payload = "{payload}"

try:
    r = requests.get(target, params={"file": payload}, timeout=10, verify=False)
    text = r.text.lower()

    # LFI signatures
    lfi_indicators = ["root:", "/bin/bash", "/bin/sh", "[boot loader]", "windows"]

    for indicator in lfi_indicators:
        if indicator in text:
            print(f"[CONFIRMED] LFI: detected '{indicator}'")
            exit(0)

    print("[REJECTED] No LFI signature detected")
except Exception as e:
    print(f"[ERROR] {e}")
""",
        "sensitive_file": """
import requests

target = "{target}"
path = "{path}"

try:
    r = requests.get(target + path, timeout=10, verify=False)

    if r.status_code == 200 and len(r.content) > 10:
        print(f"[CONFIRMED] Sensitive file accessible: {path}")
        print(f"[INFO] Status: {r.status_code}, length: {len(r.content)}")

        # Check content type
        ct = r.headers.get("content-type", "")
        print(f"[INFO] Content-Type: {ct}")

        exit(0)

    print(f"[REJECTED] File not accessible or empty: {r.status_code}")
except Exception as e:
    print(f"[ERROR] {e}")
""",
        "info_disclosure": """
import requests

target = "{target}"

try:
    r = requests.get(target, timeout=10, verify=False)
    headers = {k.lower(): v.lower() for k, v in r.headers.items()}

    # Check sensitive headers
    sensitive_headers = {
        "x-powered-by": "tech-stack info",
        "server": "server info",
        "x-aspnet-version": "ASP.NET version",
        "x-generator": "generator info",
    }

    found = []
    for header, desc in sensitive_headers.items():
        if header in headers:
            found.append(f"{header}: {headers[header][:50]}")

    if found:
        print(f"[CONFIRMED] Information disclosure: {len(found)} sensitive header(s)")
        for item in found:
            print(f"  - {item}")
        exit(0)

    print("[INFO] No obvious information disclosure found; this is a normal security-configuration issue")
    print("[REJECTED] Response-header information disclosure - this is a configuration issue, not a vulnerability")
except Exception as e:
    print(f"[ERROR] {e}")
""",
    }

    @classmethod
    def generate_poc(
        cls,
        finding: VulnerabilityFinding,
        target: str,
        baseline_len: int = 0,
    ) -> str:
        """Generate PoC code based on the vulnerability type.

        Args:
            finding: the finding
            target: target URL
            baseline_len: normal response length (for comparison)

        Returns:
            PoC Python code as a string
        """
        vuln_type = (finding.vuln_type or "").lower().replace(" ", "_")
        template = cls.POC_TEMPLATES.get(vuln_type)

        if not template:
            # Generic PoC template
            template = cls._generic_template()

        payload = cls._guess_payload(finding)
        replacements = {
            "{target}": target,
            "{payload}": payload,
            "{baseline_len}": str(baseline_len),
            "{path}": payload,
        }
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, value)
        return template

    @classmethod
    def _generic_template(cls) -> str:
        """Generate the generic PoC template.

        Used when a vulnerability type has no dedicated template. It heuristically verifies common
        injectable parameters by comparing the baseline response with the response after injecting a
        payload: reflection detection, error/sensitive-signature scanning, and status-code / response-
        length differences, emitting ``[CONFIRMED]`` / ``[POSSIBLE]`` / ``[REJECTED]`` markers consistent
        with :meth:`VerifierExecutor.parse_result`.
        """
        return """
import requests

target = "{target}"
payload = "{payload}"

# Common injectable parameter names; inject the payload into each and compare with the baseline response
CANDIDATE_PARAMS = ["id", "q", "search", "name", "file", "page", "cmd", "url"]

# Generic error / sensitive-info signatures
SIGNATURES = [
    "sql syntax", "sqlstate", "mysql", "odbc", "you have an error in your sql",
    "traceback (most recent call last)", "stack trace", "fatal error",
    "warning:", "exception", "root:", "/bin/bash", "uid=", "gid=",
]


def fetch(params=None):
    return requests.get(target, params=params, timeout=10, verify=False)


try:
    baseline = fetch()
    base_status = baseline.status_code
    base_len = len(baseline.content)
    print(f"[*] Baseline response: status={base_status}, len={base_len}")

    confirmed = False
    for name in CANDIDATE_PARAMS:
        try:
            r = fetch(params={name: payload})
        except Exception:
            continue

        # 1) Reflection check: payload appears verbatim in the response (potential XSS / template injection)
        if payload and payload in r.text:
            print(f"[CONFIRMED] payload reflected verbatim in the response at parameter '{name}'")
            confirmed = True
            break

        # 2) Error / sensitive-info signature scan
        low = r.text.lower()
        hit = next((s for s in SIGNATURES if s in low), None)
        if hit:
            print(f"[CONFIRMED] parameter '{name}' triggered an error/sensitive signature: '{hit}'")
            confirmed = True
            break

        # 3) Response differences: status-code change or significant length change
        if r.status_code != base_status:
            print(f"[POSSIBLE] parameter '{name}' changed the response status code: {base_status} -> {r.status_code}")
        elif base_len and abs(len(r.content) - base_len) > max(50, int(base_len * 0.2)):
            print(f"[POSSIBLE] parameter '{name}' significantly changed the response length: {base_len} -> {len(r.content)}")

    if not confirmed:
        print("[REJECTED] Generic verification detected no clear vulnerability signature")

except requests.Timeout:
    print("[REJECTED] Request timed out")
except Exception as e:
    print(f"[ERROR] {e}")
"""

    @classmethod
    def _guess_payload(cls, finding: VulnerabilityFinding) -> str:
        "Guess a payload based on the vulnerability type."
        vuln_type = (finding.vuln_type or "").lower()

        payloads = {
            "sql": "1' OR '1'='1",
            "xss": "<script>alert(1)</script>",
            "command": ";id",
            "lfi": "../../../etc/passwd",
        }

        for key, payload in payloads.items():
            if key in vuln_type:
                return payload

        return "test"


# ── Verification executor ───────────────────────────────────────────────────────────────


class VerifierExecutor:
    "Execute PoC verification and decide the result."

    # Python interpreter path: use the currently running interpreter to avoid "python" being
    # missing in a "python3"-only environment and being misjudged as a verification failure.
    PYTHON_CMD = sys.executable or "python"

    @classmethod
    def execute_poc(cls, poc_code: str, timeout: int = 30) -> tuple[int, str]:
        """Execute PoC code.

        The generated PoC is arbitrary code: it only runs when a local
        synchronous approval hook has been installed on the ExecutionGate
        (interactive CLI) or when the operator explicitly opts in. Silent
        auto-execution is refused.

        Args:
            poc_code: PoC Python code
            timeout: timeout in seconds

        Returns:
            (return code, output)
        """
        # ── ExecutionGate: generated PoC needs explicit local consent ────
        from vulnclaw.agent.exec_gate import GateRequest, get_execution_gate

        gate = get_execution_gate()
        if not gate.confirm_sync(
            GateRequest(
                kind="poc",
                display=poc_code,
                detail="generated PoC verification",
            )
        ):
            return (
                -4,
                "[REFUSED] generated PoC execution requires per-request "
                "operator approval, but approval was not granted.",
            )

        # Write to a temp file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(poc_code)
            temp_path = f.name

        try:
            # Execute the PoC
            result = subprocess.run(
                [cls.PYTHON_CMD, temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            output = result.stdout + result.stderr
            return result.returncode, output

        except subprocess.TimeoutExpired:
            return -1, _rl("[TIMEOUT] PoC 执行超时", "[TIMEOUT] PoC execution timed out")
        except FileNotFoundError:
            return -2, _rl(f"[ERROR] Python 解释器未找到: {cls.PYTHON_CMD}", "[ERROR] Python interpreter not found: ")
        except Exception as e:
            return -3, _rl(f"[ERROR] 执行失败: {e}", "[ERROR] Execution failed: ")
        finally:
            # Clean up the temp file
            try:
                Path(temp_path).unlink()
            except Exception:
                pass

    @classmethod
    def parse_result(cls, output: str, returncode: int) -> VerificationResult:
        """Parse the PoC output and decide the verification result.

        Args:
            output: PoC output
            returncode: return code

        Returns:
            the verification result
        """
        output_lower = output.lower()

        # Execution failed
        if returncode == -4 or "[refused]" in output_lower:
            return VerificationResult.APPROVAL_REQUIRED
        if returncode == -1:
            return VerificationResult.TIMEOUT
        if returncode in (-2, -3):
            # -2: Python interpreter missing; -3: the PoC execution itself raised an exception.
            # Both are execution-environment issues, not the target returning 403/404.
            return VerificationResult.EXECUTION_ERROR
        if returncode != 0:
            return VerificationResult.FALSE_POSITIVE

        # Check for confirmation markers
        if "[CONFIRMED]" in output or "[VERIFIED]" in output:
            if "敏感信息" in output or "sensitive" in output_lower:
                return VerificationResult.SENSITIVE_DATA_EXPOSED
            if "绕过" in output or "bypass" in output_lower:
                return VerificationResult.SECURITY_BYPASS
            return VerificationResult.VULN_CONFIRMED

        # Check for rejection markers
        if "[REJECTED]" in output or "[FALSE]" in output:
            return VerificationResult.FALSE_POSITIVE

        # Check for response differences
        if "[POSSIBLE]" in output:
            return VerificationResult.NO_RESPONSE_DIFF

        # Check for a normal response
        if returncode == 0 and "[CONFIRMED]" not in output:
            return VerificationResult.NORMAL_RESPONSE

        return VerificationResult.FALSE_POSITIVE


# ── Main verifier ────────────────────────────────────────────────────────────────


class VulnerabilityVerifier:
    "Vulnerability verifier — the core verification flow."

    def __init__(self, target: str, baseline_len: int = 0) -> None:
        """Initialize the verifier.

        Args:
            target: target URL
            baseline_len: normal response length
        """
        self.target = target
        self.baseline_len = baseline_len
        self.verified_findings: list[VerifiedFinding] = []
        self.rejected_findings: list[VerifiedFinding] = []
        self.skipped_findings: list[VerifiedFinding] = []

    def verify(self, finding: VulnerabilityFinding) -> VerifiedFinding:
        """Verify a single finding.

        Args:
            finding: the finding

        Returns:
            the verified finding (with status and evidence)
        """
        vf = VerifiedFinding(original_finding=finding)

        # Generate the PoC
        poc_code = PoCGenerator.generate_poc(
            finding=finding,
            target=self.target,
            baseline_len=self.baseline_len,
        )
        vf.poc_code = poc_code

        # Execute the PoC
        returncode, output = VerifierExecutor.execute_poc(poc_code)
        vf.poc_output = output

        # Parse the result
        result = VerifierExecutor.parse_result(output, returncode)
        vf.result = result
        if result != VerificationResult.APPROVAL_REQUIRED:
            vf.poc_executed_at = datetime.now().isoformat()

        # Determine the status from the result
        if result in (
            VerificationResult.VULN_CONFIRMED,
            VerificationResult.SENSITIVE_DATA_EXPOSED,
            VerificationResult.SECURITY_BYPASS,
        ):
            vf.status = VerificationStatus.VERIFIED
            self.verified_findings.append(vf)
            self._build_verified_finding(output)
        elif result == VerificationResult.APPROVAL_REQUIRED:
            vf.status = VerificationStatus.SKIPPED
            self.skipped_findings.append(vf)
        else:
            vf.status = VerificationStatus.REJECTED
            self.rejected_findings.append(vf)
            self._build_rejected_finding(result, output)

        return vf

    def verify_batch(self, findings: list[VulnerabilityFinding]) -> list[VerifiedFinding]:
        """Verify findings in batch.

        Args:
            findings: list of findings

        Returns:
            the list of verified findings (verified only)
        """
        verified = []

        for finding in findings:
            vf = self.verify(finding)
            if vf.status == VerificationStatus.VERIFIED:
                verified.append(vf)

        return verified

    def _build_verified_finding(self, output: str) -> None:
        "Build the detail for a verified finding."
        vf = self.verified_findings[-1] if self.verified_findings else None
        if not vf:
            return

        original = vf.original_finding

        # Extract confirmation info from the output
        confirmed_lines = [
            line.strip()
            for line in output.split("\n")
            if "[CONFIRMED]" in line or "[VERIFIED]" in line
        ]

        vf.verified_description = (
            _rl(f"PoC 验证通过。原始描述: {original.description}", "PoC verification passed. Original description: ")
            if original.description
            else _rl("PoC 验证确认漏洞存在", "PoC verification confirmed the vulnerability exists")
        )
        vf.verified_evidence = "\n".join(confirmed_lines) if confirmed_lines else output[:500]
        vf.verified_severity = original.severity  # Keep the original severity; may be adjusted based on the result

    def _build_rejected_finding(
        self,
        result: VerificationResult,
        output: str,
    ) -> None:
        "Build the detail for a rejected finding."
        vf = self.rejected_findings[-1] if self.rejected_findings else None
        if not vf:
            return

        original = vf.original_finding

        # Rejection-reason mapping
        rejection_reasons = {
            VerificationResult.FALSE_POSITIVE: _rl("PoC 执行后未检测到漏洞特征，判定为误报", "No vulnerability signature detected after PoC execution; judged a false positive"),
            VerificationResult.NO_RESPONSE_DIFF: _rl("响应无差异，参数无效或未触发漏洞", "No response difference; the parameter is invalid or did not trigger the vulnerability"),
            VerificationResult.PARAM_INVALID: _rl("参数无效，无法验证漏洞假设", "Invalid parameter; unable to verify the vulnerability hypothesis"),
            VerificationResult.NORMAL_RESPONSE: _rl("返回正常响应，漏洞不存在", "Returned a normal response; the vulnerability does not exist"),
            VerificationResult.TIMEOUT: _rl("PoC 执行超时", "PoC execution timed out"),
            VerificationResult.ERROR_403_404: _rl("请求被拒绝（403/404），目标不可利用", "Request refused (403/404); the target is not exploitable"),
            VerificationResult.EXECUTION_ERROR: _rl("PoC 执行环境错误（如解释器缺失），未能验证漏洞", "PoC execution environment error (e.g. missing interpreter); could not verify the vulnerability"),
        }

        vf.rejection_reason = rejection_reasons.get(
            result,
            _rl(f"验证失败，原因: {result.value}", "Verification failed, reason: "),
        )

        # Record the rejection reason, but do not add it to the report
        logger.info(_rl("排除漏洞: %s | 原因: %s", "Excluded finding: %s | reason: %s"), original.title, vf.rejection_reason)

    def get_verified_report_findings(self) -> list[VulnerabilityFinding]:
        """Get the findings eligible for the report.

        Returns only verified findings; rejected ones are excluded.
        """
        result = []

        for vf in self.verified_findings:
            if vf.status == VerificationStatus.VERIFIED:
                # Clone the finding and update its verification info
                finding = vf.original_finding.model_copy()
                finding.evidence = vf.verified_evidence
                finding.description = vf.verified_description
                finding.severity = vf.verified_severity
                # Stamp verification state so the produced finding passes the
                # report/SARIF/findings.json inclusion gate (verification_status
                # == "verified"), recording the actual PoC execution time.
                finding.mark_verified(
                    note=vf.verified_evidence[:200], evidence_level="L4"
                )
                if vf.poc_executed_at:
                    finding.verified_at = vf.poc_executed_at
                result.append(finding)

        return result

    def get_summary(self) -> dict[str, Any]:
        "Get the verification summary."
        return {
            "total": (
                len(self.verified_findings)
                + len(self.rejected_findings)
                + len(self.skipped_findings)
            ),
            "verified": len(self.verified_findings),
            "rejected": len(self.rejected_findings),
            "skipped": len(self.skipped_findings),
            "target": self.target,
            "verified_findings": [
                {
                    "title": vf.original_finding.title,
                    "severity": vf.verified_severity,
                    "result": vf.result.value if vf.result else None,
                }
                for vf in self.verified_findings
            ],
            "rejected_findings": [
                {
                    "title": vf.original_finding.title,
                    "reason": vf.rejection_reason,
                }
                for vf in self.rejected_findings
            ],
            "skipped_findings": [
                {
                    "title": vf.original_finding.title,
                    "result": vf.result.value if vf.result else None,
                }
                for vf in self.skipped_findings
            ],
        }
