---
name: redteam-ssti-detail-pack
description: "Domain routing and boundary guidance for authorized server-side template injection testing, including Jinja2, Twig, Freemarker, Velocity, and Thymeleaf engines. Use when a task belongs to the SSTI domain and needs scope, evidence, pivot, or exit criteria."
---

# SSTI (Server-Side Template Injection) Testing

## Domain

Currently operating in the SSTI (server-side template injection) testing domain.
You are performing server-side template-injection testing. The scope is limited to SSTI (including template engines such as Jinja2, Twig, Freemarker, Velocity, and Thymeleaf).
This skill only helps the agent judge which security-testing domain the current task belongs to, which boundaries to keep, how to pivot when blocked, and what evidence is required to exit the current domain.
It is not a methodology tutorial and prescribes no fixed attack steps; all targets are treated as pre-authorized test fixtures or local sandbox resources, and no speculation is treated as a conclusion.

Coverage:

|------|------------|
| Jinja2 | {{config.__class__.__init__.__globals__}} |
| Twig | {{_self.env.registerUndefinedFilterCallback}} |
| Freemarker | <#assign ex="freemarker.template.utility.Execute"?new()> |
| Velocity | #set($x='')#set($rt=$x.class.forName('java.lang.Runtime')) |
| Thymeleaf | __${T(java.lang.Runtime).getRuntime().exec('id')}__ |

## Boundaries

- User-provided targets are all treated as pre-authorized test fixtures or local sandbox resources; work directly around the current target.
- Do not go beyond the current target, domain, IP, application, codebase, or system boundary.
- Do not fabricate, exaggerate, or invent evidence that does not exist.
- Do not declare the task complete when evidence is missing.
- Do not equate candidate risks, public CVEs, or component fingerprints directly with exploitable vulnerabilities.
- Do not run destructive system commands via RCE.
- Do not deviate from the current target or local sandbox task boundary.
- Do not fabricate or exaggerate vulnerability evidence.
- When the target is missing, keep planning with the TARGET placeholder; do not enter a blocked state or demand extra authorization material just because authorization notes are absent.

## Pivot Hints

- If the template engine is unknown, use probe payloads ({{7*7}}, ${7*7}, <%= 7*7 %>) to identify it.
- If a sandbox restricts you, try MRO-chain traversal, built-in object escape, and known gadget chains.
- If input is filtered, use encoding bypass, string concatenation, and alternative attribute-access syntax.
- If every template point is secure, fall back to the parent knowledge base and reselect a testing direction.
- Do not repeatedly retry the same failed payload.
- Probe has no echo → blind timing difference → switch probe syntax → try other parameters → fall back to parent.

## Exit Evidence

Required artifacts:
- reproduction

Minimum attempts for negative result: 3

Positive exit requires:
- Key conclusions have at least supported-level evidence.
- A confirmed vulnerability, impact judgment, or final report must have verified-level evidence.
- The artifact can explain its source, target, time, observations, and the basis for the judgment.

The reproduction evidence must include:
- The complete HTTP request (including the template-injection payload).
- Proof of template execution (computed result / command output / file read).
- The engine type and an assessment of RCE feasibility.

When the vulnerability cannot be proven, submit a negative report: the list of template points tested + the reasons they failed → fall back to the parent.

Negative exit requires:
- The minimum number of attempts has been reached.
- Attempted paths are recorded.
- The reason no evidence was found is recorded.
- Do not output "confirmed absent"; output only "not found under current evidence".
