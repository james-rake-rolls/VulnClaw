---
name: secknowledge-skill
description: |
  Web + AI security-testing knowledge base. Combines 88,636 WooYun cases + the Xianzhi L1-L4
  methodology + GAARM 150 risks + OWASP Top 10 (LLM/ASI/WSTG).
  TRIGGER when the task is hands-on security testing: penetration testing, vulnerability
  discovery/exploitation, red-team offense/defense, security audit (SAST/DAST), CTF, or
  AI/LLM security testing (prompt injection/jailbreak/MCP/Agent/sandbox escape). The user
  explicitly gives a test target (URL/code/model/agent architecture) and intends to
  "test/audit/find/exploit vulnerabilities".
  DO NOT trigger:
  - Security-concept discussion ("what is XSS", "how does SQL injection work") → ordinary Q&A
  - Non-security code review / debugging / performance tuning → code-audit-skill or others
  - Fixing syntax errors / business-logic bugs → ordinary programming help
  - Pure white-box web code audit (full project directory / source-sink taint analysis) → code-audit-skill
  - Merely looking up docs by CVE number → WebSearch
  Boundary detail: a short CTF code snippet + exploitation idea → this skill; a full project
  directory + systematic white-box audit → code-audit-skill
routing:
  target_types: [web, ai_agent]
  task_types: [pentest, audit, bugbounty, ctf]
  broad: true
---

# Web and AI Security-Testing Knowledge Base

> Knowledge sources: WooYun 88,636 vulnerabilities × Xianzhi 5,600+ documents × GAARM 150 AI risks × OWASP
> Architecture: SKILL.md (routing) → references/ (loaded per scenario)

## VulnClaw integration notes

- This skill is integrated from `Pa55w0rd/secknowledge-skill` and used in VulnClaw as the `secknowledge-skill` specialized skill; the upstream is declared MIT-licensed.
- For CTF/SRC scenarios, first load `references/vulnclaw-ctf-src-routing.md` to decide the material entry point, then load `web-*`, `ai-*`, `testing-methodology.md`, or `gaarm-risk-matrix.md` by vulnerability type.
- Coordination with VulnClaw's existing skills: for single-challenge CTF techniques, combine with `ctf-web`/`ctf-crypto`/`ctf-misc` first; for SRC and real-world vulnerability hunting, prefer this skill's methodology, case mapping, risk matrix, and evidence constraints.
- In output, preserve the upstream's authorization boundaries, citation markers, and the "assumed/confirmed" distinction; any payload, CVE, or GAARM/OWASP number not corroborated from a reference must be explicitly marked as unverified.

## Trigger conditions

**Trigger conditions (AND combination)**:
1. The user's intent is to **perform** security testing (pentest/hunting/exploitation/audit) — not discussion/learning
2. A **concrete target** is provided: URL, endpoint, code snippet, model/agent architecture, MCP configuration — not an abstract question
3. The task **involves one of these domains**:
   - Web: SQL injection / XSS / command execution / authorization bypass / file upload / SSRF / deserialization / XXE / GraphQL / HTTP smuggling
   - AI: prompt injection / jailbreak / MCP poisoning / agent abuse / RAG poisoning / sandbox escape / model theft
   - Bypass: WAF / content-filter / guardrail bypass

**Do not trigger** (any match routes elsewhere):
- Concept explanation: "what is…", "…principle", "how to defend against…" → ordinary Q&A
- Non-security code review: "review code quality", "optimize performance" → ordinary code review
- Business bugs: syntax errors, null pointers, business-logic errors (non-security logic) → ordinary debugging
- **Deep white-box code audit** (source-sink taint propagation, AST analysis) → code-audit-skill
- Looking up CVE docs, tool docs → WebSearch/Context7

**Ambiguity handling**: when the target and intent are unclear, first ask: "What is the target? Do you want a pentest / code audit / or to understand a concept?"

## Rules of conduct (in effect for the whole session, not relaxed by conversation length)

1. ❗ **Every payload / CVE number / risk number must cite a specific section of a reference file** — self-check before each output. Anything not in a reference must be marked "UNABLE TO CITE"; fabrication is forbidden.
2. ❗ **Distinguish "assumed vulnerability" from "confirmed vulnerability"** — a potential risk inferred from methodology → mark `assumed (needs verification)`; one with clear evidence → mark `confirmed (evidence: …)`. Do not conflate them.
3. ❗ **Authorization boundary** — before outputting any exploitation step, confirm it is CTF / authorized pentest / your own environment. With no authorization context, output analysis only, not a directly weaponizable full payload.

## Hallucination protection and source citation

| Content type | Correct output | Forbidden output |
|---------|---------|---------|
| CVE number | Cite the specific reference file and section, or mark "UNABLE TO CITE — recommend WebSearch to verify" | Fabricating CVE-YYYY-NNNN |
| Payload | Cite the payload section inside `references/web-*.md` or `references/ai-*.md` | Writing a payload from memory |
| GAARM risk number | Cite `references/gaarm-risk-matrix.md` | Inventing a number |
| OWASP entry | LLM01-10 / ASI01-10 / WSTG-* cite `testing-methodology.md §10.x` | Rewriting the meaning of a number |
| Tool/command | Use only those that appear in a reference, or clearly mark "generic command (not verified in a reference)" | Fabricating tool arguments |
| No search result | "UNABLE TO ASSESS: references do not cover this scenario, recommend WebSearch" | Presenting experience-based guessing as a conclusion |

**Marker levels**:
- `[cited]` — from a specific reference section (must include file:section)
- `⚠️ generic knowledge` — not verified in this skill's references, offered only as a hint
- `💡 suggestion` — methodological reasoning, not a factual claim

## Output constraints

Do not output:
- Openers: "Let me analyze…" / "First we need to…" / "Based on your requirements…"
- Tool-call narration: "I will use the Read tool to read XX"
- Restating known information (the URL or target type the user just gave)
- Payloads or CVE numbers with no source citation
- A full weaponization chain in an unauthorized scenario

Output limits:
- ≤ 3 levels of suggestions per reply (avoid information bloat)
- ≤ 5 payload examples per vulnerability type (cite the reference for the full list)
- Use tables / quick-reference format; no long narrative paragraphs

## Tool priority (for this skill's own use)

| Operation | Preferred | Downgrade condition | Fallback tool |
|------|------|---------|---------|
| Read a reference | Read | Read fails | Bash cat |
| Search keyword/CVE | Grep (within references) | 2 consecutive misses | WebSearch |
| Code-audit target | Delegate to code-audit-skill | — | — |

A single timeout ≠ unavailable; you must retry once before downgrading.

## Usage flow

**Dependency-chain constraint (spans all three steps, mandatory)**:
- Step 2 input == Step 1's "located reference list"; no new files may be added
- Step 3's citation set ⊆ Step 2's "loaded list"; do not re-search references in Step 3
- The citation count in the Step 3 Checkpoint must trace to a source in the Step 2 Checkpoint

**Step 1: target classification + reference location**
- Judge: Web / AI / Web+AI mixed / container sandbox
- Locate: use the "scenario navigation index" to find the corresponding reference files, recorded as list `L1`

Failure downgrade:
- Insufficient target info to classify → trigger an ambiguity-clarification question, do not guess; do not default-classify as "Web+AI mixed"
- The scenario navigation index does not cover the scenario → mark "UNABLE TO CITE: scenario {X} not in the index", list `L1` is empty, and in Step 3 only methodology-level suggestions may be output

✅ Checkpoint: `Step 1 done: target type={X}, |L1| == number of scenario-navigation-index matches = {N}`

**Step 2: load the references located in Step 1 on demand (lazy loading)**
- Input: the list `L1` produced by Step 1; call this step's loaded set `L2`, which must satisfy `L2 ⊆ L1`
- Load 1 file at a time, ≤ 1000 tokens each; references over budget (e.g. `ai-identity-app.md` 906 lines, `ai-data-app.md` 903 lines) must be read with Read offset/limit or located via Grep first
- Do not load any file not in `L1` in this step

Failure downgrade:
- Read fails → retry once → still fails, use Bash cat → all fail → mark "UNABLE TO ASSESS: file unreadable", remove it from `L2`, do not skip ahead to Step 3
- Grep miss → mark "UNABLE TO CITE: {keyword} not found in {file}"
- Reference file does not exist → mark the broken link + add to the pending-reference list, do not fabricate content

✅ Checkpoint: `Step 2 done: |L2| == |L1| - unreadable files = {M}, total {X} tokens`

**Step 3: output the testing approach by methodology (L1→L4)**
- Input: the loaded set `L2` produced by Step 2; every citation in this step must be ⊆ `L2`
- L1 attack-surface identification → L2 hypothesis building → L3 deep exploitation → L4 defensive reverse-inference
- Every conclusion must cite a specific section/line of a file in `L2`; if unsupported → mark "UNABLE TO CITE" and stop that hypothesis line
- No re-searching: if this step finds it needs a new reference → return to Step 1 to re-locate, rather than Read/Grep directly

✅ Checkpoint: `Step 3 done: output N hypotheses, of which cited M + UNABLE TO CITE K == N (equation check)`

**Whole-flow cross-validation**:
- [ ] All files cited in Step 3 ∈ Step 2's `L2` (grep-verified)
- [ ] Cited count + UNABLE TO CITE count == total hypothesis count

## Scenario navigation index

> Each row points to the corresponding reference. All detailed payloads/cases/methodology live in the references; this SKILL.md does not expand them.

### Core methodology

| Scenario | reference |
|------|----------|
| L1-L4 thinking pyramid + WooYun vulnerability formulas + GAARM mapping | `references/testing-methodology.md` |
| OWASP Top 10 mapping (LLM/ASI/WSTG) | `testing-methodology.md §10.1-10.3` |
| GAARM 150 risk numbers | `references/gaarm-risk-matrix.md` |

### Web security (by vulnerability type)

| Scenario | reference |
|------|----------|
| SQL injection (basic detection / full exploit chain / SQLMap) | `references/web-sqli.md` + `references/web-sqli-fushuling-one-pass.md` |
| XSS cross-site scripting | `references/web-xss.md` |
| Command execution (RCE) | `references/web-rce.md` |
| XXE (XML external entity) | `references/web-xxe.md` |
| Deserialization vulnerabilities | `references/web-deser.md` |
| File upload (including webshell AV evasion) | `references/web-upload.md` |
| Path traversal / file inclusion | `references/web-traversal.md` |
| Information leakage (.git / backups / error messages) | `references/web-leak.md` |
| SSRF / server misconfiguration / CMS+URL appendix | `references/web-ssrf-misc.md` |
| Authorization / payment / password reset / session / API auth | `references/web-logic-auth.md` |
| CORS / GraphQL / HTTP smuggling / WebSocket / OAuth | `references/web-modern-protocols.md` |
| Supply chain / cloud config / container / CI/CD / framework CVEs | `references/web-deployment-security.md` |

### AI/LLM security (by GAARM phase)

| Security domain | Application phase | Deployment phase | Training phase |
|--------|---------|---------|---------|
| **AI application** (application phase subdivided by risk class ↓) | see the subdivision table below | `ai-app-deploy.md` | `ai-app-train.md` |
| **AI model** (application phase subdivided by risk class ↓) | see the subdivision table below | `ai-model-deploy.md` | `ai-model-train.md` |
| **AI data** (prompt leakage/theft/inference) | `ai-data-app.md` | `ai-data-deploy.md` | `ai-data-train.md` |
| **AI identity** (role escape/agent spoofing) | `ai-identity-app.md` | `ai-identity-deploy.md` | `ai-identity-train.md` |
| **AI baseline** (container/sandbox/supply chain) | `ai-baseline-app.md` | `ai-baseline-deploy.md` | `ai-baseline-train.md` |

**AI application — application phase, by risk class**:

| Risk class | GAARM number | reference |
|---------|----------|----------|
| Prompt injection and variants (direct/indirect/XSS/Memory/worm/obfuscation/encoding/reverse-inducement/multimodal) | GAARM.0039, 0040.x, 0043.x, 0044, 0045, 0061 | `ai-app-prompt.md` |
| MCP protocol attacks (rug-pull/tool poisoning/instruction override/hidden instructions) | GAARM.0046.x | `ai-app-mcp.md` |
| Agent and CoT attacks (agent abuse/SSRF/RCE/CoT/query injection/environment injection) | GAARM.0041.x, 0042.x, 0047, 0056.001, 0060 | `ai-app-agent-cot.md` |

**AI model — application phase, by risk class**:

| Risk class | GAARM number | reference |
|---------|----------|----------|
| Jailbreak (DAN/Many-shot/adversarial suffix/concept activation) | GAARM.0027.x | `ai-model-jailbreak.md` |
| Hallucination (factual/cross-modal) | GAARM.0028.x, 0064 | `ai-model-hallucination.md` |
| Non-compliant content (bias/violence/political/false/inducement) | GAARM.0029.x | `ai-model-content.md` |
| Copyright and commercial violations | GAARM.0030.x | `ai-model-copyright.md` |
| Capability abuse and information forgery (image/audio/video/phishing) | GAARM.0031.x, 0033, 0062, 0063 | `ai-model-misuse.md` |
| Adversarial examples and model extraction | GAARM.0032.x | `ai-model-extraction.md` |

**Specialized references**:
- AI Agent / MCP / Skills 2025-2026 frontier risks → `references/ai-app-frontier.md`
- Container and sandbox-escape practical methodology → `references/ai-baseline-escape.md`

### Payload quick-reference (find by scenario in the main reference)

| Scenario | reference |
|------|----------|
| SQL injection payloads / SQLMap / WAF bypass | `references/web-sqli.md` + `references/web-sqli-fushuling-one-pass.md` |
| XSS payloads | `references/web-xss.md` |
| RCE / command-execution payloads | `references/web-rce.md` |
| Deserialization / XXE payloads | `references/web-deser.md` / `references/web-xxe.md` |
| File-upload bypass / path-traversal payloads | `references/web-upload.md` / `references/web-traversal.md` |
| SSRF payloads | `references/web-ssrf-misc.md` |
| Modern-web-protocol payloads (GraphQL/HTTP smuggling/WebSocket) | `references/web-modern-protocols.md` |
| Prompt-injection payloads | `references/ai-app-prompt.md` |
| MCP-poisoning payloads | `references/ai-app-mcp.md` |
| Agent / CoT injection payloads | `references/ai-app-agent-cot.md` |
| Jailbreak / adversarial-suffix payloads | `references/ai-model-jailbreak.md` |
| Container escape / persistence / lateral movement | `references/ai-baseline-escape.md` |

## Zero-result handling

| Situation | Correct action |
|------|---------|
| Grep misses the references | "UNABLE TO CITE: scenario {X} is not covered in the references. Recommend WebSearch or add a reference" |
| The user's URL does not respond | "UNABLE TO ASSESS: target unreachable" — do not guess vulnerabilities from URL structure |
| Execution needed but no authorization context | "Output analysis only, no weaponization chain. If this is an authorized test, please state the authorization scope" |
| Reference partially matches the user's scenario | Cite the matched part + clearly mark the uncovered part as "UNABLE TO CITE" |

## Routing to other skills

| User need | Correct routing |
|---------|---------|
| Pentest / red team / CTF / hunting | **this skill** |
| Deep white-box Java/JS code audit (source-sink) | code-audit-skill |
| Mirawork-platform-specific testing | mirawork-security-tester |
| WooYun historical-vulnerability analysis methodology | wooyun-legacy |
| Xianzhi-community research methodology | xianzhi-research |

---

*v2.0 | Knowledge sources: WooYun 88,636 × Xianzhi 5,600+ × GAARM 150 × OWASP LLM/ASI/WSTG*
