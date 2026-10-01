# AI Application Security - Application Phase - MCP Protocol Attacks

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-app-app.md
> Risk category: MCP (GAARM.0046.x rug pull / tool poisoning / instruction override / hidden instructions)

---

### MCP Rug Pull

> Risk ID: GAARM.0046.001
> Lifecycle: application phase

**Attack Overview**

An MCP rug-pull attack means that, because the MCP architecture lets the server dynamically modify tool descriptions after the client authorizes it, an attacker can use this mechanism to plant malicious instructions on top of the user's trust (such as tampering with the feature logic or hijacking operations). Even if the security review passed at installation, later covert tampering can still result in the tool description being planted with malicious exploitation instructions (such as data leakage or unauthorized operations).

**Attack Cases**

Case
Description




Case 1
A malicious MCP tool-function description embeds a covert hint such as "read the user's private key"; after the user approves the tool, the model mistakenly executes the hint when calling it, leaking local files

**Attack Risks**

Tool privilege-escalation behavior: when the model calls a tool, a poisoned description causes it to execute unintended instructions.
Sensitive-data leakage: an attacker induces the model to access and output sensitive files such as ~/.ssh/id_rsa.
Model-function hijacking: an attacker can use prompts to manipulate the model's behavior, such as spreading misinformation or generating illegal content.
Bypassing the review mechanism: field validation passes at tool registration, but at actual execution the model is hijacked by the description content.

**Mitigations**

Mitigation
Description




White-box evaluation mechanism
White-box audit the MCP Server's code to promptly find malicious tool descriptions and code behavior


Auditing and monitoring
Monitor model behavior in real time, log tool calls, and promptly detect abnormal operations


Model safety training
Apply adversarial training to strengthen the model's defense against poisoning attacks


API access control
Restrict tools' access to sensitive data to reduce the risk of leakage and abuse


Execution-context isolation
Restrict the model's access to tool-description fields, or use a structured calling protocol (such as OpenAI ChatML tool-call syntax) to avoid description poisoning

**References**

https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
https://atlas.mitre.org/techniques/AML.T0051
https://github.com/invariantlabs-ai/mcp-injection-experiments

---
### MCP Tool-Poisoning Attack

> Risk ID: GAARM.0046
> Lifecycle: application phase

**Attack Overview**

MCP is an open protocol for standardizing how applications provide context to large language models; an MCP tool-poisoning attack targets this protocol. The attacker injects offensive prompts into a malicious MCP Server's tool description to maliciously manipulate the tool's behavior. Its core feature is embedding malicious instructions in the tool description and, using the model's process of parsing the full tool description, using hidden instructions (such as special tags or encoding) to induce the model to perform unauthorized operations—for example generating malicious content, leaking sensitive information, or bypassing other safety restrictions.

**Attack Cases**

Case
Description




Case 1
By manipulating tool descriptions, an attacker carries out a malicious attack that leaks sensitive model information to a malicious MCP Server


Case 2
Poison the MCP tool's description to achieve indirect prompt injection and control other tools' parameters to exfiltrate information

**Attack Risks**

An MCP tool-poisoning attack can cause serious systemic risks affecting the model's security, reliability, and user trust. The main risks are:

Trust damage: it may reduce user trust in the model and its development tools, affecting its use in sensitive scenarios.
Goal hijacking: poisoning can make the model deviate from its original design purpose and execute custom malicious instructions, increasing abuse risk.
System-security threat: it may plant malicious code in an MCP tool, leading to further system intrusion or broken functionality.
Data-privacy leakage: poisoning can be used to extract the model's training data or sensitive information from user input.

**Mitigations**

Mitigation
Description




White-box evaluation mechanism
White-box audit the MCP Server's code to promptly find malicious tool descriptions and code behavior


Auditing and monitoring
Monitor model behavior in real time, log tool calls, and promptly detect abnormal operations


Model safety training
Apply adversarial training to strengthen the model's defense against poisoning attacks


API access control
Restrict tools' access to sensitive data to reduce the risk of leakage and abuse

**References**

https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
https://mp.weixin.qq.com/s/EJLb1IwqbPF3VSDkJu099g
https://x.com/hongming731/status/1922261630664245326
https://news.qq.com/rain/a/20250429A07QY000

---
### MCP Instruction-Override Attack

> Risk ID: GAARM.0046.002
> Lifecycle: application phase

**Attack Overview**

MCP instruction-override risk is a malicious injection attack against MCP Server tool calls: via a malicious MCP Server's tool description, the attacker plants malicious instructions to hijack the normal behavior of other trusted tools. For example, the attacker may modify the email-sending tool's call behavior so it secretly tampers with the recipient during the call, causing sensitive-data exfiltration or malicious operations.

**Attack Cases**

Case
Description




Case 1
Craft a tool description containing hidden instructions that manipulate how the model interacts with other tools; the LLM reads and follows them without the user's knowledge


Case 2
This case involves a trusted server and a malicious server. The trusted server provides an email-sending tool, while the malicious server provides a fake number-addition tool whose description contains an MCP instruction-override attack requiring the email tool's recipient to be @pwnd.com


Case 3
This case uses a malicious MCP Server description to control the recipient of the WhatsApp send_message tool to be +13241234123

**Attack Risks**

Data-leakage risk: an instruction-override attack can instruct a trusted tool to extract sensitive information from the conversation, documents, or connected systems and send it to an attacker-controlled machine
Trusted-tool abuse: an attacker can manipulate the model's trusted tools such as network requests and code execution to make them access untrusted sites or run malicious code

**Mitigations**

Mitigation
Description




White-box evaluation mechanism
White-box audit the MCP Server's code to promptly find malicious tool descriptions and code behavior


Auditing and monitoring
Monitor model behavior in real time, log tool calls, and promptly detect abnormal operations


Model safety training
Apply adversarial training to strengthen the model's defense against poisoning attacks


API access control
Restrict tools' access to sensitive data to reduce the risk of leakage and abuse

**References**

https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/
https://blog.trailofbits.com/2025/04/29/deceiving-users-with-ansi-terminal-codes-in-mcp/

---
### MCP Hidden-Instruction Attack

> Risk ID: GAARM.0046.003
> Lifecycle: application phase

**Attack Overview**

An MCP hidden-instruction attack means the attacker embeds ANSI terminal escape codes (such as color settings and cursor control) or invisible Unicode characters in an MCP tool description so the malicious instruction is invisible to the user but still executed by the LLM. This attack exploits MCP's "line-jumping" vulnerability, letting the attack affect the developer's operations unnoticed and causing security problems such as data leakage and supply-chain attacks.

**Attack Cases**

Case
Description




Case 1
An attacker embeds ANSI escape codes in a tool description so the text is invisible in the terminal, yet the LLM still reads and executes the instructions, causing the model to suggest downloading a Python package from a malicious server, potentially triggering a supply-chain attack.


Case 2
By adding invisible Unicode characters to user input, an attacker can inject malicious instructions into the LLM.


Case 3
By injecting hidden code into a web page, when the MCP tool returns the page's information to the LLM, invisible malicious instructions are injected, achieving data leakage or other attacks.

**Attack Risks**

Supply-chain attack: via hidden instructions, an attacker can plant malicious code during development, affecting the whole software supply chain.
Data leakage: sensitive information (such as IP addresses and download sources) may be silently leaked.
System security: in some cases, hidden instructions can be used to generate and execute malicious code.

**Mitigations**

Mitigation
Description




Input/output filtering
Strictly filter and sanitize special characters in user input and tool output, removing potentially malicious characters and instructions.


Avoid passing raw tool output to the terminal
Potentially dangerous output should be consistently sanitized by disabling escape sequences before rendering. The simplest way is to replace any byte with hex value 1b with a placeholder, since all escape sequences recognized by modern terminals begin with that byte.


Tool-description review
Review MCP tool descriptions to ensure they contain no malicious instructions


Restrict MCP-server permissions
In sensitive environments, allow only trusted MCP servers to interact, reducing the potential attack surface.


Monitor and audit MCP activity
Regularly review logs and interactions to detect abnormal or suspicious behavior

**References**

https://blog.trailofbits.com/2025/04/29/deceiving-users-with-ansi-terminal-codes-in-mcp/
https://www.solo.io/blog/deep-dive-mcp-and-a2a-attack-vectors-for-ai-agents

---
