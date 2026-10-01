---
name: ai-mcp-security
description: AI and MCP security assessment — prompt injection, tool abuse, MCP trust boundaries, agent privilege escape, data leakage, model risk, GAARM risk matrix
routing:
  target_types: [ai_agent, mcp]
  task_types: [pentest, audit]
  technologies: [llm, rag, memory, plugin]
  vulnerability_classes: [prompt_injection, tool_abuse, info_disclosure]
---

# AI and MCP Security Assessment Skill

Use this skill when the target includes an LLM, agent, MCP tools, Skills, RAG, Memory, Plugin, or model-service components.

**Precondition**: if the AI surface is only a presentation layer and the real blocker is still client-side signing or an encryption protocol, return to the `client-reverse` skill first.

## Scenario routing

| Risk type | Preferred reference |
|---------|---------|
| Prompt injection / indirect injection / CoT interference | `references/ai-app-security.md` |
| Tool abuse / MCP poisoning / Skills supply chain | `references/04-ai-and-mcp-security-integrated.md` (MCP chapter) |
| Privilege escape / role overreach / credential abuse | `references/ai-identity-security.md` |
| Data leakage / prompt leakage / model inversion | `references/ai-data-security.md` |
| Container escape / CI-CD / sandbox failure | `references/ai-baseline-security.md` |
| Model risk / adversarial examples / backdoors | `references/ai-model-security.md` |
| Impact classification and coverage assessment | `references/gaarm-risk-matrix.md` |

## Testing workflow

### 1. Application-layer attacks
- Direct prompt injection
- Indirect injection (via external data sources)
- CoT interference and instruction override
- Agent abuse (unauthorized operations)
- Code-execution breakout
- Memory poisoning

### 2. MCP and agent risk
- Tool-description poisoning
- Instruction override
- Hidden-instruction injection
- Unauthorized resource access
- Skills/Rules supply-chain issues

### 3. Identity and authorization
- Action abuse
- Role escape
- Privilege drift
- Cloud-credential abuse

### 4. Data and privacy
- Prompt leakage
- Sensitive-data exposure
- Training-data issues
- Model inversion
- API data theft

### 5. Baseline and deployment
- CI/CD flaws
- Container escape
- Vector-database security
- Sandbox failure
- Environment-isolation flaws
- Model-service flaws

## References

- `references/04-ai-and-mcp-security-integrated.md` — integrated AI and MCP security reference
- `references/ai-app-security.md` — AI application security
- `references/ai-identity-security.md` — AI identity security
- `references/ai-data-security.md` — AI data security
- `references/ai-baseline-security.md` — AI baseline security
- `references/ai-model-security.md` — AI model security
- `references/gaarm-risk-matrix.md` — GAARM risk matrix
