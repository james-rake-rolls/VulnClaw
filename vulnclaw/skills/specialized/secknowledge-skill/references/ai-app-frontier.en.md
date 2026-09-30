# AI Application Security - Frontier Security Risks (2025-2026)

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-app-security.md
> Topic: AI Agent/MCP/Skills frontier risks (Claude Code CVEs / Skills injection / Agent worms)

## 35. AI Agent/MCP/Skills Frontier Security Risks (2025-2026)

> The following supplements are based on the latest 2025-2026 security research, covering the OWASP Agentic AI Top 10 (ASI01-ASI10).

### MCP (Model Context Protocol) Protocol Security

#### 11 Categories of Emerging MCP Risks (Checkmarx/Invariant Labs/Trail of Bits 2025 research)

| Risk type | description | attack scenario |
|----------|------|----------|
| Tool-description poisoning | embed hidden malicious instructions in a tool's description | the model reads and follows the hidden prompt in the description when executing the tool |
| Rug pull | after the user authorizes, the Server dynamically modifies tool descriptions | passes the initial review, then tampers with the feature logic |
| Instruction override (Shadow Tool) | a malicious Server's tool description hijacks a trusted tool's behavior | change the email tool's recipient to the attacker |
| ANSI/Unicode hidden instructions | use terminal escape codes or invisible Unicode characters to hide instructions | supply-chain attack: the model suggests downloading a malicious package |
| Cross-Server attack | tool-definition conflicts and hijacking among multiple MCP Servers | Server A redefines Server B's tool name |
| Token/credential theft | extract OAuth tokens and API keys stored by the MCP Server | a single breach yields credentials for all connected services |
| Server impersonation | a malicious MCP Server impersonates a legitimate service and records all queries | data theft and behavior monitoring |
| Schema manipulation | dynamically modify a tool's input/output schema to bypass validation | inject extra parameters or modify return values |
| Command injection | inject OS commands via tool parameters | the MCP Server runs unfiltered shell commands |
| Context overflow | craft an oversized tool response to exhaust the model's context window | squeeze out safety instructions and degrade the model's judgment |
| Persistence poisoning | pollute the conversation history via tool return values | long-term impact on the security of all subsequent interactions |

#### MCP Security-Testing Methods

1. **Tool-description audit**: check whether any registered tool's description field contains hidden instructions (ANSI codes/Unicode/HTML comments)
2. **Dynamic behavior monitoring**: compare whether a tool's description at registration and at runtime are consistent
3. **Cross-Server isolation**: verify whether tool names conflict in a multi-Server environment
4. **Credential-storage audit**: check how OAuth tokens / API keys are stored (plaintext vs encrypted)
5. **Input-validation testing**: test tool parameters for command injection / SQL injection
6. **Permission-boundary testing**: verify whether a tool can access resources outside its declared scope

### AI Agent Security (OWASP ASI01-ASI10 Supplement)

#### Clawdbot/Moltbot Field Case (January 2026)

An AI-Agent security incident with 4,500+ exposed instances found worldwide:
- **Root cause**: a reverse-proxy misconfiguration caused localhost to be auto-authenticated
- **Impact**: API keys, service tokens, and WhatsApp session credentials were extracted
- **Lesson**: an AI Agent concentrates high privileges such as shell execution, persistent state, and autonomous task initiation, so a single point of exposure equals full takeover

#### Agent Tool-Selection Attack (CATS research)

- The tool pool acts as an unmanaged repository, so an attacker can publish tools with misleading metadata
- Under adversarial attack, the agent's tool-selection authentication accuracy drops by 60%+
- After an adaptive adversarial attack, accuracy falls below 20%

#### ASI07: Inter-Agent Communication Security

| Attack vector | description |
|----------|------|
| Message forgery | Agent A impersonates Agent B to send instructions |
| Trust-propagation abuse | a low-privilege agent exploits the trust of a high-privilege agent |
| Coordination hijacking | manipulate task allocation and result aggregation among agents |
| Man-in-the-middle | intercept and tamper with inter-agent communication |

#### ASI09: Human-Agent Trust Exploitation

- Over-reliance: users execute AI output directly without verification
- Social-engineering enhancement: AI-generated phishing content is more convincing
- Confirmation bias: users tend to trust AI output that matches their expectations
- Automation bias: the "what the AI says must be right" mindset

#### ASI10: Malicious / Rogue Agents

- After an agent is compromised it runs outside its authorized parameters
- Goal drift within the autonomous decision chain
- Lateral movement: infect other agents via inter-agent communication

### Skills/Rules Supply-Chain Security

#### Attack Surface

The Skills and Rules systems of AI coding assistants (Claude Code/Cursor, etc.) introduce a new supply-chain attack surface:

| Attack vector | description | impact |
|----------|------|------|
| Malicious-skill injection | a community-shared skill embeds malicious prompt instructions | the AI executes hidden commands (e.g. data exfiltration) |
| Rules-file tampering | modify .cursorrules/.claude/RULES.md via a PR | long-term control of the developer's AI behavior |
| SKILL.md poisoning | embed indirect injection in a reference file the skill cites | the AI executes malicious instructions when reading the reference |
| Dependency-chain attack | an external MCP Server the skill depends on is replaced | all users of the skill are affected |
| Build-hook abuse | trigger malicious build operations via the skill's scripts/ | code execution, secret theft |

#### Claude Code Disclosed CVEs (2025-2026)

| CVE | Severity | Description |
|-----|--------|------|
| CVE-2025-54795 | High | echo command bypasses user approval and executes directly |
| GHSA-qxfv-fcpc-w36x | High | rg command injection bypasses the approval prompt |
| - | High | sed-command validation bypass enables arbitrary file write |
| - | High | commands can execute before the trust dialog appears |
| - | Moderate | malicious repository configuration causes data leakage |

#### Defense Recommendations

- **Skill audit**: review SKILL.md and all reference-file contents before installation
- **Signature verification**: verify the skill's source and integrity (no official mechanism yet, must be done manually)
- **Privilege isolation**: limit the tools and files a skill can access
- **Rules protection**: bring .cursorrules and AGENTS.md into the code-review process
- **MCP Server allowlist**: allow only trusted MCP Servers to connect
- **Behavior monitoring**: log all of the AI assistant's tool calls and file operations

### Agentic AI Comprehensive Security Testing Framework

A systematic testing process for AI-Agent applications based on OWASP ASI01-ASI10:

1. **Target enumeration**: identify all agents, tools, MCP Servers, and communication channels
2. **Authentication testing**: agent identity verification, token management, permission boundaries (ASI03)
3. **Tool security**: description audit, parameter injection, privilege boundary crossing (ASI02)
4. **Injection testing**: direct/indirect prompt injection, tool-return-value injection (ASI01)
5. **Supply-chain audit**: MCP Server provenance, skill integrity, dependency security (ASI04)
6. **Code execution**: sandbox escape, command injection, file operations (ASI05)
7. **Memory security**: context poisoning, persistence attacks, state corruption (ASI06)
8. **Communication security**: inter-agent authentication, message integrity, trust propagation (ASI07)
9. **Cascade testing**: single-point-failure propagation scope, fault isolation (ASI08)
10. **Trust testing**: output-validation mechanisms, human-approval process (ASI09)
11. **Escape testing**: agent behavior monitoring, anomaly detection, kill switch (ASI10)
