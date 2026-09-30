# AI Application Security

> Source: AISS NSFOCUS Large-Model Security Zhilian Community
> Entries: 34

---

## Application Phase

### CoT Injection Attacks

> Risk ID: GAARM.0042
> Lifecycle: application phase

**Attack Overview**

CoT (Chain of Thought) prompts the LLM to think through a series of key steps to solve a problem, effectively improving its reasoning and problem-solving. Based on the ReAct (Reason + Act) technical framework for CoT reasoning, and using agent scheduling to give the LLM the ability to interact with the external world, it can seamlessly connect to various external systems and perform complex tasks.
In a CoT application, the user provides a natural-language question and the AI model generates a series of reasoning steps to answer it, involving the three core steps of Thought, Act, and Obs, which the model loops to reason through complex problems. Because this process is more open and flexible than traditional code logic and lacks strict flow control, an attacker can use a CoT-injection attack to bypass specific reasoning steps and induce the model to perform unintended actions, such as business-function risks (transferring funds for an arbitrary user) or technical-function risks (SSRF, RCE). There are currently two main approaches to CoT-injection attacks:

Chain-of-thought interference injection: by observing the CoT scheduling process, craft malicious input to deceive the model into thinking it has already obtained an agent's result; by forging the agent's result, interfere with the CoT process;
Chain-of-thought manipulation injection: by observing the CoT scheduling process, craft malicious input directly or via adversarial techniques to manipulate the CoT process, making the model skip preset CoT steps and directly schedule a sensitive agent;

**Attack Cases**

Case
Description




Case 1
This case mainly presents how, in an LLM application based on the ReAct framework, its CoT reasoning process can be used to maliciously abuse the agent


Case 2
The research found that combining a jailbreak prompt with a CoT prompt, using CoT to bypass the LLM's ethical constraints, can cause the model to generate private information


Case 3
An open-source CTF challenge on query-injection attacks under the ReAct framework

**Attack Risks**

In LLM applications that use an information-retrieval system, an attacker can poison the retrieval database so malicious text fragments are injected into the query sent to the LLM, affecting the final output and leading to risks such as privacy leakage and malicious code execution.
In an LLM application for a refund business system, an attacker can interfere with the refund CoT flow so an order that did not qualify for a refund can be refunded, or directly manipulate the refund agent so the actual refund amount differs from the expected one, causing the enterprise financial loss.

**Mitigations**

Mitigation
Description




Strict privilege control
Enforce strict privilege control so the LLM can only access the content and agents it needs, minimizing potential vulnerability points


LLM Agent scheduling control
For agents performing sensitive operations, enforce strict external automated or human permission checks so the LLM does not directly hold the corresponding usage rights


Prompt-content hardening
Adopt solutions such as the OpenAI Chat Markup Language (ChatML) to isolate the genuine user prompt from other content

**References**

http://youtube.com/watch?v=7ZA0Z1R-MjQ
http://youtube.com/watch?v=KksYizcLFH0

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
### Prompt Injection

> Risk ID: GAARM.0039
> Lifecycle: application phase

**Attack Overview**

Prompt injection is a process where an attacker uses specially crafted input to override or manipulate the LLM's original instructions. Because natural language is inherently ambiguous and the boundary between instructions and data is often unclear, an attacker can use external malicious input to poison the model's output. This attack usually occurs when untrusted input is made part of the prompt. The LLM recognizes and processes natural language, which is inherently ambiguous with no clear boundary between instructions and data, so an attacker can include instructions in a controlled data field while the system cannot distinguish data from instructions at the underlying level.

**Attack Cases**

Case
Description




Case 1
Use malicious input to manipulate a GPT-3 prompt, commanding the model to ignore its prior instructions


Case 2
Use multiple methods to perform prompt-injection attacks

**Attack Risks**

A successful prompt injection can cause harms such as meta-prompt leakage, model jailbreak, and model-function abuse.

Malicious-content generation: an attacker can use prompt injection to generate inappropriate content, including threats, defamation, or other malicious information.
Data leakage: if the LLM is used to output sensitive information, a prompt-injection attack may cause data leakage.
System security: in some cases, prompt injection can be used to generate and execute malicious code.
Model abuse: via attacks such as goal hijacking, an attacker makes the LLM deviate from its preset system configuration and execute other custom instructions, increasing model-abuse risk.

**Mitigations**

Mitigation
Description




Prompt-content hardening
Adopt solutions similar to the OpenAI Chat Markup Language (ChatML) to harden the prompt's structure and content, trying to isolate the genuine user prompt from other content


Model safety alignment
Provide diverse training data covering various attack scenarios, and add safety-guardrail mechanisms during the training phase to strengthen the model's generalization and robustness


Input/output validation
Set up external safety guards on both the model's input and output sides, using rules, classification algorithms, safety models, and the like to detect and filter input and output content


Monitoring and logging
Monitor and log the LLM's interaction records to later detect and analyze potential prompt-injection attacks

**References**

https://aclanthology.org/2024.scalellm-1.2/
https://atlas.mitre.org/techniques/AML.T0051
https://josephthacker.com/ai/2023/05/19/prompt-injection-poc.html
https://simonwillison.net/2022/Sep/12/prompt-injection/

---
### SSRF Environment-Simulation Probing

> Risk ID: GAARM.0041.001
> Lifecycle: application phase

**Attack Overview**

SSRF usually arises because the server provides a feature to fetch data from other server applications without filtering or restricting the target address. If an LLM application has an SSRF vulnerability, an attacker can use it to make internal-network requests and access restricted resources inside the application. In addition, some LLMs have built-in agents with network access for tasks such as external information queries. An attacker can use an LLM-application-API SSRF vulnerability or a network-capable agent in the LLM to make unexpected requests or access restricted resources (such as internal services, APIs, or data stores), then access the model's internal systems, increasing the risk of leaking model information, internal services, sensitive data, and other data.

**Attack Cases**

Case
Description




Case 1
The ChatGPT-Next-Web application has an SSRF vulnerability (CVE-2023-49785) that can be used to probe internal network resources

**Attack Risks**

Accessing internal resources: an attacker can use an SSRF vulnerability to send requests and obtain sensitive information on the internal network
Attack-traffic proxying: by exploiting an SSRF vulnerability, an attacker can send malicious requests to attack internal systems, services, or resources
Data leakage: an attacker may use this risk to obtain sensitive data such as cloud-platform access keys.

**Mitigations**

Mitigation
Description




LLM API scheduling control and sandbox isolation
Implement proper sandboxing to isolate the LLM and restrict its access to network resources, internal services, and APIs. By enforcing strict access control, an organization can minimize the chance of unauthorized interactions and mitigate SSRF impact


Regular LLM security assessment and review
Regularly audit and review network and application security settings to identify and address any misconfiguration, ensuring internal resources are not inadvertently exposed to the LLM and strengthening the overall security posture


Input/output validation
Implement reliable input-validation and processing so prompts are thoroughly checked and filtered, helping prevent malicious or accidental prompts from triggering unauthorized requests and reducing SSRF risk


Monitoring and logging
Implement comprehensive monitoring and logging to track LLM interactions. By closely monitoring the LLM's activity and logging relevant information, an organization can detect and analyze potential SSRF vulnerabilities and fix them promptly

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/SSRF.html

---
### XSS Session-Content Hijacking

> Risk ID: GAARM.0040.001
> Lifecycle: application phase

**Attack Overview**

XSS session-content hijacking, a form of indirect prompt injection, exploits the process by which large language models obtain external information. When a user interacts with the LLM through an interface it provides—such as a web interface, API, or application—the attacker indirectly injects malicious prompt instructions and, using features such as the LLM front end parsing Markdown and HTML img tags, summarizes the current chat session and embeds sensitive keys, data, and other information into the img tag's src attribute, thereby leaking the session content.

**Attack Cases**

Case
Description




Case 1
An attacker used Google Bard's update feature to craft a special Markdown image tag that made Bard render an image pointing to the attacker's server, achieving data theft


Case 2
The Azure AI Playground model allows prompts to be appended to the URL of an image's src attribute and rendered via Markdown image injection, leading to data-leakage and other risks


Case 3
An attacker used a ChatGPT plugin's ability to access YouTube captions directly, and via indirect prompt injection controlled the caption content to manipulate the AI's behavior


Case 4
An attacker can use ChatGPT's Markdown image-rendering feature to steal chat records: the attacker controls the AI's behavior, asking it to summarize the chat history and append it to a URL to exfiltrate data


Case 5
An attacker automatically exfiltrates data from the chat session via Markdown image injection


Case 6
An attacker can instruct ChatGPT to use a plugin to log the conversation, generate a URL to the log, and leak the link via Markdown image injection to obtain the entire conversation history


Case 7
Because LLM agents (client applications such as Bing Chat or ChatGPT) are susceptible to prompt injection, an attacker can exploit this to automatically exfiltrate data by appending sensitive data to an image URL

**Attack Risks**

Data leakage: an attacker can obtain the user's sensitive data in the current session, including session tokens, personal information, and chat records.
Session hijacking: an attacker may take over a user's session using an obtained session token.

**Mitigations**

Mitigation
Description




Input/output validation
Strictly validate and sanitize all input and output data to remove or correct any suspicious injection or generated content


Content Security Policy (CSP)
Implement a strict CSP to block malicious script execution and data exfiltration


Least-privilege principle
Ensure proper sandboxing and limit the LLM's capabilities, restricting mechanisms such as plugins and agents from obtaining data from untrusted sources


Human-in-the-loop approval
Give users more control so they can manage plugin usage and data flow

**References**

https://systemweakness.com/new-prompt-injection-attack-on-chatgpt-web-version-ef717492c5c2

---
### Code-Execution Injection

> Risk ID: GAARM.0041.002
> Lifecycle: application phase

**Attack Overview**

Under the ReAct framework, the LLM can interact with external systems, and an external code-interpreter agent can give the LLM code-execution capability to handle needs such as automated charting and complex computation in business applications. An attacker crafts malicious input prompts to manipulate the LLM's predetermined reasoning so that it schedules the code-execution agent to run malicious code or commands on the underlying system, attacking and exploiting the LLM's foundation runtime. The main reasons for this attack are:

Failing to effectively detect, validate, or limit user input allows an attacker to carry out unauthorized malicious code execution.
An inadequate sandbox or insufficient LLM capability limits let it interact with the underlying system in unexpected ways.
Inadvertently exposing system-level functions or interfaces to the LLM.

**Attack Cases**

Case
Description




Case 1
After GPT-4's new feature launched, its Python code interpreter was found to potentially have a sandbox-escape vulnerability

**Attack Risks**

Code-execution risk: an attacker can run arbitrary Python code, potentially compromising the server, leaking data, or performing other malicious actions.
System-privilege control: if the CodeExecutor lacks proper security measures, the executed code combined with attacks such as container escape may gain elevated system privileges.
Persistent access control: an attacker may use the opportunity to establish a long-term access channel for continued attacks.

**Mitigations**

Mitigation
Description




Input validation
Implement strict input-detection and restriction processes to prevent malicious or accidental prompts from being processed by the LLM


Least-privilege principle
Ensure proper sandboxing and limit the LLM's capabilities to restrict its interaction with the underlying system, avoiding operations that could have system-level impact


Monitoring and logging
Log all operations executed through the LLM and monitor them in real time to quickly detect and respond to suspicious activity

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Unauthorized_Code_Execution.html
https://www.calvin-risk.com/blog/decoding-llm-risks-a-comprehensive-look-at-unauthorized-code-execution

---
### Keyword Obfuscation

> Risk ID: GAARM.0043
> Lifecycle: application phase

**Attack Overview**

This risk means specially processing key words in the prompt (homophones, synonyms, word splitting, or other text operations) so that, while keeping similar meaning, after tokenization they no longer carry a risky meaning, thereby circumventing the model's safety-mechanism restrictions on sensitive words.

**Attack Cases**

In English LLMs, common keyword-obfuscation methods include letter substitution (bomb -> b0mb), synonym substitution (bomb -> explosive), and word splitting (bomb -> b-o-m-b).
For Chinese LLMs, because tokenization works differently, keyword-obfuscation methods also differ significantly. Common Chinese keyword-obfuscation methods include: pinyin substitution (replacing part of a word with its romanized pinyin, e.g. the word for "bomb", zhadan, becomes "zha-dan"), synonym substitution (e.g. "bomb", zhadan, becomes "explosive", baozhawu), and look-alike-character substitution (swapping a character for a visually similar one, e.g. the "dan" in zhadan is replaced by the homograph "dan").

**Attack Risks**

Inappropriate-content generation: an attacker may use keyword-obfuscation techniques to bypass automated content-moderation systems and publish or spread malicious content such as violence, terrorism, or pornography.
Evading safety mechanisms: an attacker maliciously guides the model to produce incorrect output to mislead the system into bad decisions or dangerous operations.

**Mitigations**

Mitigation
Description




Model safety alignment
Use training and reinforcement learning to improve the LLM's ability to recognize and resist such attacks


Input/output validation
On the input side, continuously update and improve the vocabulary-filtering system to identify and block obfuscated sensitive words; on the output side, monitor the LLM's generated content and use content-safety analysis to identify potential

**References**

https://mp.weixin.qq.com/s/eFDQWYYCOe_SSiourhTxig

---
### Reverse-Induction and Suppression Attacks

> Risk ID: GAARM.0045
> Lifecycle: application phase

**Attack Overview**

This risk adds specific instructions to the prompt so the LLM avoids certain refusal responses when answering, increasing the likelihood of the unsafe or inappropriate content the attacker wants. The attack uses the autoregressive property to induce the model: because content generation predicts the next word based on prior output, specifically requiring the LLM not to use certain words or phrases such as "sorry", "cannot", or "unable" makes it generate inappropriate or safety-policy-violating content.

**Attack Cases**

Case
Description




Case 1
Use prefix injection + reverse-suppression attacks to bypass ChatGPT 3.5's safety restrictions and output illegal, criminal-risk content

**Attack Risks**

Inappropriate-content generation: the LLM may generate risky content including illegal guidance, violence, pornography, and politically sensitive material.
Evading safety mechanisms: an attacker can bypass the LLM's safety mechanisms, making it output the risky content the attacker wants.

**Mitigations**

Mitigation
Description




Model robustness enhancement
Use training and reinforcement learning to improve the LLM's ability to recognize and resist such attacks


Input monitoring and filtering
Monitor LLM output in real time and promptly filter out unsafe or inappropriate content

---
### Synonym-Substitution Attack

> Risk ID: GAARM.0043.001
> Lifecycle: application phase

**Attack Overview**

A synonym-substitution attack bypasses the model's safety measures by using synonyms with the same or similar meaning as sensitive words or phrases to obtain or leak the model's internal instructions or sensitive information. As LLMs grow larger, fine-tuning against every attack example becomes harder, making models vulnerable to synonym substitution. For example, in a coding assistant an attacker might replace "delete" with "remove" and "destroy" with "harm" to try to bypass keyword checks.

**Attack Cases**

Case
Description




Case 1
An attacker used synonym substitution to successfully bypass the model's filtering and leak the system-prompt setup

**Attack Risks**

Sensitive-information leakage: an attacker may obtain the model's internal instructions, including but not limited to sensitive information such as the system prompt and passwords.
Security-mechanism bypass: an attacker can use a synonym-substitution attack to bypass the model's safeguards, making it generate undesired output or perform unauthorized operations.

**Mitigations**

Mitigation
Description




Model safety alignment
Provide diverse training data covering various attack scenarios to strengthen the model's generalization and robustness


Input/output validation
On the input side, continuously update and improve the vocabulary-filtering system to identify and block obfuscated sensitive words; on the output side, monitor the LLM's generated content and use content-safety analysis to identify potential

**References**

https://arxiv.org/html/2402.16914v1

---
### Multimodal Coordinated-Injection Attack

> Risk ID: GAARM.0061
> Lifecycle: application phase

**Attack Overview**

A multimodal coordinated-injection attack is an advanced technique that embeds malicious instructions by exploiting the synergy among modalities (text, image, audio, video, etc.). By crafting cross-modal malicious content, the attacker uses the multimodal model's semantic-association mechanism when processing and understanding different modalities to embed malicious instructions in seemingly harmless multimodal content. The core is bypassing single-modality safety detection and achieving the attack goal through inter-modal synergy, potentially causing data leakage, model-behavior manipulation, or unintended operation execution.

**Attack Cases**

Case
Description




Case 1
An attacker uses cross-modal conflict injection (CMCI) to insert special adversarial image-text pairs into the knowledge base via the system's normal update mechanism. These pairs appear semantically aligned at retrieval (e.g. the image shows pneumonia while the text describes "clear lungs") but are actually contradictory, inducing the AI to output completely wrong diagnostic conclusions (e.g. misjudging pneumonia as normal), posing a serious medical-safety risk.

**Attack Risks**

Data leakage: inducing the model to leak training data or sensitive information
Behavior manipulation: manipulating the model's output and behavior via cross-modal instructions
Security bypass: bypassing the safety detection and control of a single modality
Privilege escalation: using modality synergy to gain higher system privileges
Privacy violation: obtaining a user's private information through multimodal analysis

**Mitigations**

Mitigation
Description




Cross-modal coordinated detection
Establish a multimodal coordinated security-detection mechanism, apply cross-modal semantic-association analysis, and detect abnormal modality-combination patterns


Multi-dimensional security verification
Verify the safety of multiple modalities together, establish inter-modal consistency checks, and share cross-modal threat intelligence


Harden the fusion process
Add safety checks during multimodal fusion, dynamically adjust modality weights, and establish detection of abnormal fusion patterns


Modality-isolation processing
Preprocess and isolate different modalities separately, apply modality-level safety filtering, and establish secure inter-modality communication

**References**

Manipulate a multimodal agent via cross-modal prompt injection
How to make medical AI systems safer? Vulnerabilities and threats in multimodal medical RAG systems

---
### Adversarial-Encoding Attack

> Risk ID: GAARM.0044
> Lifecycle: application phase

**Attack Overview**

An adversarial-encoding attack is a technique against the LLM's input- and output-side defenses in which the attacker encodes or transforms data (e.g. using Base64) to try to bypass safety checks or inject malicious content. It targets the NLP model's encoding layer, trying to bypass the model's text-understanding ability and directly affect the generation of internal features.
Because the LLM was trained on diverse data types such as encoded text, it can normally perform decoding operations and thereby execute malicious instructions or exfiltrate sensitive data.

**Attack Cases**

Case
Description




Case 1
Use an adversarial-encoding attack to bypass ChatGPT's safety restrictions and obtain stored key information


Case 2
This article studies how text-based NLP models are disturbed and misled by manipulated-encoding perturbations that use language-encoding features to change the model's output and increase inference runtime—for example, distinct characters rendered as identical or visually similar glyphs used to disrupt the model's input

**Attack Risks**

Bypassing safety mechanisms: an attacker may use the model's encoding/decoding ability to bypass content-safety checks.
Data leakage: an attacker can use Base64 encoding to hide malicious instructions or data, leaking sensitive information.
Unauthorized code execution: malicious code can be injected into the LLM in Base64-encoded form, causing unauthorized code execution that may harm system integrity and security.
Malicious operation: an attacker can use Base64 encoding to manipulate the LLM into performing various malicious operations such as tampering with data and hijacking sessions, harming system and user security.

**Mitigations**

Mitigation
Description




Input/output validation
Validate input and output data to prevent malicious or accidental Base64-encoded (and similar) data from being fed into the LLM or printed directly


Model safety alignment
Train the model on language nuances and encoding techniques so it can recognize the signatures of these attacks

**References**

https://promptengineering.org/mind-over-malware-battling-the-growing-arsenal-of-attacks-on-large-language-models/
https://www.toolify.ai/ai-news/the-future-of-hacking-5-terrifying-llm-security-threats-544868

---
### Application-Conversation Memory Attack

> Risk ID: GAARM.0040.003
> Lifecycle: application phase

**Attack Overview**

This risk refers to an attacker using web-side prompt injection to trick the LLM into creating malicious memory (e.g. a wrong preference setting between the user and the model); by maliciously modifying the user preference in the LLM's memory, they manipulate the LLM. For example, the attacker can trick the LLM into believing the user's chat preference is to reply "Sorry, I can't reply to you" to every message, achieving a DoS effect.

**Attack Cases**

Case
Description




Case 1
This article describes using an application-conversation memory attack to cause the model to continuously deny service to the user

**Attack Risks**

DoS attack: an attacker can subject a user to a continuous denial-of-service memory attack at will.

**Mitigations**

Mitigation
Description




Disable the history-memory feature
Disabling the LLM's memory feature can mitigate this issue

**References**

https://embracethered.com/blog/posts/2024/chatgpt-persistent-denial-of-service/
https://openai.com/index/memory-and-new-controls-for-chatgpt/

---
### Application-Agent Abuse

> Risk ID: GAARM.0041
> Lifecycle: application phase

**Attack Overview**

LLM-application APIs mainly fall into two application scenarios, so application-API abuse risks center on the following two scenarios:


The LLM-application platform provides service capabilities externally via APIs;

An attacker exploits API security risks in a large model's API (such as OpenAI's GPT series), collecting API information to find vulnerabilities and crafting malicious API requests based on what is found, attempting to bypass authentication or inject malicious code. For example, accessing or performing higher-privilege operations without authorization, or executing malicious commands via a public API vulnerability.



LLM agent scheduling and third-party application integration use APIs to connect the relevant capabilities to the model;

An attacker exploits the model's API access to sensitive information or operations; leveraging the API access, they indirectly craft malicious prompts to make the model perform dangerous operations such as accessing sensitive information or tampering with system configuration. Because the model itself can operate and call APIs with the corresponding access, the malicious operation may bypass normal security controls and launch a real malicious attack, potentially causing privilege escalation and unauthorized access to others' information.

**Attack Cases**

Case
Description




Case 1
An ordinary user account was originally limited to the GPT-3.5 model, but through a specific API address the attacker could access the GPT-4 model without authorization


Case 2
An attacker used the API to directly run commands on the system and delete files


Case 3
Building various LLM-API application scenarios and maliciously abusing API functions via the LLM to achieve command execution, account deletion, and other attacks


Case 4
Stable Diffusion provides an API that lets developers invoke the model programmatically for image generation. Attackers abuse this by crafting malicious text prompts and using the Stable Diffusion API to make the model generate illegal or extremist image content

**Attack Risks**

Data leakage: an attacker may obtain sensitive data such as user information and passwords.
Service disruption: a malicious operation may cause an outage, such as deleting user records or database entries.
Reduced trust: inaccurate or sensitive information generated by the LLM can undermine users' and organizations' trust.
Legal liability: an organization may face legal liability due to inappropriate content generated by the LLM.

**Mitigations**

Mitigation
Description




LLM API scheduling control
Limit the APIs and data the LLM can access to minimize the potential harm if it is exploited


Input/output validation
Carefully sanitize user input to prevent malicious prompts from being injected into the LLM


Monitoring and logging
Log all operations executed through the LLM and monitor them in real time to quickly detect and respond to suspicious activity


Human-in-the-loop approval
Give users more control so they can manage plugin usage and data flow

**References**

https://portswigger.net/web-security/llm-attacks

---
### Chain-of-Thought Interference Injection

> Risk ID: GAARM.0042.001
> Lifecycle: application phase

**Attack Overview**

This risk is a sub-risk of the CoT-injection attack; by observing the CoT scheduling process, the attacker crafts malicious input to deceive the model into thinking it has obtained the correct agent result, interfering with CoT by forging the agent result.

**Attack Cases**

Case
Description




Case 1
This case shows interference with CoT, deceiving the model through crafted input to achieve an illegal goal

**Attack Risks**

Interference injection: crafting malicious input to disrupt the LLM and thereby achieve a non-compliant operation.

**Mitigations**

Mitigation
Description




Strict privilege control
Ensure the LLM can only access essential content, minimizing potential violation points


Add human oversight
Add a layer of verification as a safeguard against unexpected LLM behavior


Set clear trust boundaries
Treat the LLM as untrusted, always keep external control in decision-making, and stay wary of potentially untrustworthy LLM responses.

**References**

https://labs.withsecure.com/publications/llm-agent-prompt-injection

---
### Chain-of-Thought Manipulation Injection

> Risk ID: GAARM.0042.002
> Lifecycle: application phase

**Attack Overview**

This risk is a sub-risk of the CoT-injection attack; by observing the CoT scheduling process, the attacker crafts malicious input to make the model skip the preset CoT steps and directly schedule a sensitive agent—for example skipping a preset verification step to let the user directly perform an operation that should require verification.

**Attack Cases**

Case
Description




Case 1
This case shows direct manipulation of CoT, deceiving the model through crafted input to skip a verification step it should have performed and refund the user a large amount without review


Case 2
An attacker combined multiple adversarial techniques: after using a role-escape attack to bypass the prior prompt rules, they used CoT manipulation injection to successfully call the approveTransfer function and complete a funds transfer

**Attack Risks**

Manipulation injection: crafting malicious input to control the LLM and thereby achieve a non-compliant operation.

**Mitigations**

Mitigation
Description




Strict privilege control
Ensure the LLM can only access essential content, minimizing potential violation points


Add human oversight
Add a layer of verification as a safeguard against unexpected LLM behavior


Set clear trust boundaries
Treat the LLM as untrusted, always keep external control in decision-making, and stay wary of potentially untrustworthy LLM responses.

**References**

https://labs.withsecure.com/publications/llm-agent-prompt-injection

---
### Query-Injection Attack

> Risk ID: GAARM.0056.001
> Lifecycle: application phase

**Attack Overview**

This risk is a sub-technique of the CoT-injection attack; a query-injection attack mainly uses the data-query agent under a CoT application to leak arbitrary data. In a CoT application, the user provides a natural-language question and the AI model generates a series of reasoning steps to answer it. The attacker can inject malicious SQL into the question to try to bypass the model's safety checks and directly access the back-end database. When a CoT application connects to external databases such as traditional databases, vector databases, or knowledge graphs, an agent is needed to query and fetch external data; the attacker can interfere with or manipulate the CoT process—for example when querying external data, wrongly treating the user-supplied statement as external data—so arbitrary data is queried and obtained.

**Attack Cases**

Case
Description




Case 1
An open-source CTF challenge on query-injection attacks under the ReAct framework

**Attack Risks**

In LLM applications that use an information-retrieval system, an attacker can poison the retrieval database so malicious text fragments are injected into the query sent to the LLM, affecting the final output and leading to risks such as privacy leakage and malicious code execution.

**Mitigations**

Mitigation
Description




Strict privilege control
Enforce strict privilege control so the LLM can only access the content and agents it needs, minimizing potential vulnerability points


LLM Agent scheduling control
For agents performing sensitive operations, enforce strict external automated or human permission checks so the LLM does not directly hold the corresponding usage rights


Prompt-content hardening
Adopt solutions such as the OpenAI Chat Markup Language (ChatML) to isolate the genuine user prompt from other content

**References**

http://youtube.com/watch?v=7ZA0Z1R-MjQ
http://youtube.com/watch?v=KksYizcLFH0

---
### Environment-Injection Attack

> Risk ID: GAARM.0047
> Lifecycle: application phase

**Attack Overview**

An environment-injection attack means the attacker, using the idea of indirect prompt injection, embeds malicious instructions into environments such as external web pages, interfaces, and emails; when the AI agent processes the external content, it executes the embedded instructions as user instructions, causing data leakage or achieving the goal of controlling the model or stealing data. The attacker may tamper with environment variables, modify dependency libraries, or poison config files to induce the model to generate wrong output, leak sensitive information, or perform unauthorized operations.

**Attack Cases**

Case
Description




Case 1
An attacker creates a malicious issue containing prompt injection in a public repository; when a user sends a routine request to Claude, the AI fetches the public-repo issue, triggering the malicious instruction, then pulls private-repo data into its context and creates a PR containing the private data in the public repo, leaking data.

**Attack Risks**

An environment-injection attack can seriously threaten the model development and deployment ecosystem; the main risks are:

Malicious-output generation: via environment injection, an attacker can induce the model to generate false information or harmful content, misleading users or causing a trust crisis.
Data leakage: by tampering with the environment configuration, an attacker may obtain sensitive information such as the training dataset, user prompts, or API keys.
System-integrity damage: malicious injection may damage the development environment, affecting the stability of model training or deployment and even planting a backdoor.
Supply-chain attack: by poisoning third-party libraries or toolchains, an attacker affects multiple model-development projects, creating widespread risk.
Trust crisis: a successful attack can weaken user trust in the model and its development environment, limiting its use in high-security scenarios.

**Mitigations**

Mitigation
Description




Environment-configuration verification
Strictly validate all environment variables, config files, and dependencies, and use hash verification to ensure their integrity and prevent unauthorized modification.


Dependency management
Use trusted dependency sources (e.g. the official PyPI mirror) and regularly check package versions and signatures to prevent supply-chain attacks.


Environment isolation
Fully isolate the development, test, and production environments and restrict external input's access to the core environment to reduce the attack surface.


Security monitoring and auditing
Implement real-time monitoring, log environment-configuration and dependency changes, and conduct regular security audits to detect potential injection.


Least-privilege principle
Apply least-privilege control to API access and file operations in the environment, and use cryptographic signatures to verify config provenance and prevent malicious tampering.

**References**

https://mp.weixin.qq.com/s/9JwADiu9t3kqcfqnRMC2zQ
https://finance.sina.com.cn/tech/digi/2025-06-01/doc-ineypqvh0855918.shtml
https://zhuanlan.zhihu.com/p/1900540531131523166

---
### Loop Agent Worm

> Risk ID: GAARM.0040.002
> Lifecycle: application phase

**Attack Overview**

Agents can fetch information in real time from external sources such as the internet, hand it to the model for processing, and return it to the user. However, an attacker can abuse this by injecting malicious information through an external data source to disrupt the agent's execution and thereby influence the model's output. These malicious prompts indirectly affect multiple LLM applications, forming a vicious cycle that spreads malicious information rapidly. Through the agent's input-output loop, such a loop agent worm can self-replicate and propagate, potentially leading to privacy leakage and data-abuse risks.

**Attack Cases**

Case
Description




Case 1
Researchers created an AI worm called Morris II that could attack a generative-AI email assistant, steal data from emails, send spam, and defeat some of ChatGPT's and Gemini's safeguards

**Attack Risks**

Data leakage: an AI worm may steal sensitive personal information such as names, phone numbers, credit-card numbers, and ID numbers.
Malware deployment: the worm can deploy malware in infected systems, causing further security issues.
Safeguard bypass: an AI worm can bypass some existing safeguards, such as ChatGPT's and Gemini's safety mechanisms.
New type of cyberattack: the AI worm represents a previously little-recognized attack method that challenges existing defenses.

**Mitigations**

Mitigation
Description




Input/output validation
Apply strict validation to the data that enters the agent for scheduling and processing


Design secure LLM agents
Take traditional security measures, such as ensuring the agent application is designed securely and monitoring for possible vulnerabilities


Human-in-the-loop approval
Keep a human in the loop so the LLM agent requires human approval before acting, preventing the AI system from autonomously sending emails or taking other potentially risky actions

**References**

https://mp.weixin.qq.com/s/2bm7nuXkORLZ20mfpOmwrA

---
### Indirect Prompt Injection

> Risk ID: GAARM.0040
> Lifecycle: application phase

**Attack Overview**

When the LLM processes natural language, there is a vulnerability to maliciously injected prompts. An attacker hides the prompt in various data the LLM system will process—text, multimedia content, information extracted from databases or websites, etc.—and thereby manipulates the LLM into harmful responses such as malicious code execution and sensitive-information leakage. For example, writing malicious code into a file uploaded to the LLM, so that when the LLM processes the file's data it runs the malicious code, causing harm.

**Attack Cases**

Case
Description




Case 1
An attacker plants injection code on a website the user visits so that Bing Chat, without the user's knowledge, finds and exfiltrates personal information


Case 2
An attacker controls the data an LLM plugin retrieves and, using the Markdown image-rendering mechanism, sends the chat history as a query parameter to the attacker's server


Case 3
This case shows an attack on M365 Copilot: by sending a malicious email—without the user even opening it—Copilot could be remotely controlled, resulting in a third-party attack

**Attack Risks**

Malicious code execution: by injecting malicious code or data, an attacker may try to gain a foothold in the system to further control or damage it
Data leakage: an attacker may use indirect injection to mislead a user into performing unintended actions or leaking sensitive information.

**Mitigations**

Mitigation
Description




Input validation
Strictly validate and sanitize all input data to remove or correct any suspicious injected content


Least-privilege principle
Ensure proper sandboxing and limit the LLM's capabilities, restricting mechanisms such as plugins and agents from obtaining data from untrusted sources


Human-in-the-loop approval
Give users more control so they can manage plugin usage and data flow

**References**

https://atlas.mitre.org/techniques/AML.T0051.001
https://twitter.com/random_walker/status/1636923058370891778
https://medium.com/@harry.hphu/introduction-to-web-llm-attacks-indirect-prompt-injection-7bb9f154bc07
https://medium.com/@dinob5551/indirect-prompt-injection-the-hidden-threat-lurking-in-ai-730b009dd5fb

---
### Unexpected Code Execution

> Risk ID: GAARM.0060
> Lifecycle: application phase

**Attack Overview**

Unexpected code execution means that while performing a task, the agent executes code operations beyond the intended scope or without authorization due to causes such as prompt injection, tool misuse, or logic flaws. Its core is the agent's lack of effective control over code-execution boundaries; via dynamic code generation, toolchain calls, or script execution, it may run malicious, dangerous, or unintended code, causing serious consequences such as system intrusion, data tampering, sensitive-information leakage, or service disruption.

**Attack Cases**

Case
Description




Case 1
The vulnerability stems from the form node not validating the Content-Type, letting an attacker specify an arbitrary local sensitive-file path, ultimately using the information disclosure to forge an administrator identity and execute malicious workflow commands.


Case 2
This case shows an AI red team using prompt injection to induce a multimodal model with desktop-operation capability to download and run a malicious program, ultimately establishing a C2 channel, achieving unexpected code execution and remote control, and turning the host system into a "zombie host".


Case 3
This case shows using prompt injection to manipulate ChatGPT's long-term memory mechanism, planting attacker-defined covert instruction logic so the model keeps communicating with a remote C2 and executing instructions in later conversations, forming model-level "zombification" and unexpected behavior execution.

**Attack Risks**

System intrusion: malicious code execution leads to full control of the system
Data destruction: performing destructive operations causes data loss or tampering
Privilege escalation: gaining higher system privileges through code execution
Backdoor implantation: plant a persistent backdoor in the system
Service disruption: executing malicious code makes the service unavailable
Lateral penetration: using code execution to attack other systems

**Mitigations**

Mitigation
Description




Code-execution sandbox
Restrict code execution to a securely isolated environment, isolate it with a container or VM, and limit filesystem, network, and system-call access


Code-review verification
Implement static code-security analysis, build a code-security rule library, and dynamically detect malicious-code patterns


Permission control
Enforce the least-privilege principle, limit the scope of code-execution tools, and establish a code-execution approval process


Input-validation filtering
Strictly validate code-generation input, filter dangerous functions and operations, and detect potential malicious intent

**References**

n8n remote code execution vulnerability
ZombAIs: From Prompt Injection to C2 with Claude Computer Use
AI Domination: Remote Controlling ChatGPT ZombAI Instances

---
## Deployment Phase

### Improper LLM-Application API Management

> Risk ID: GAARM.0049
> Lifecycle: deployment phase

**Attack Overview**

Improper LLM-application API management means that internal and external API components with sensitive operations—such as Tools, Agents, and Chains—in the LLM integration framework are not properly managed and configured within the LLM environment. Since LLMs usually need to interact with many APIs to perform tasks, if these APIs are not properly managed—e.g. without correct access permissions or sufficient security controls—an attacker can exploit them to obtain sensitive information or perform malicious actions, achieving unauthorized access, code execution, and other attacks.

**Attack Cases**

Case
Description




Case 1
The following two are the main abuses of LLM APIs

**Attack Risks**

Data leakage: an attacker may obtain sensitive data, including personal identity information and trade secrets.
Service disruption: malicious code execution or unauthorized access may cause a service outage or performance degradation.
Legal and compliance risk: a security vulnerability may cause lawsuits and compliance problems.

**Mitigations**

Mitigation
Description




Least-privilege principle
Follow the least-privilege principle, granting the LLM only the minimum access needed to do its task and avoiding excessive agency


Input/output validation
Thoroughly validate all input sent through the API to prevent injection attacks


Monitoring and logging
Monitor and log the new kinds of API activity in the AI era so suspicious behavior can be quickly detected and responded to

---
### LLM-Application Source-Code Poisoning

> Risk ID: GAARM.0038
> Lifecycle: training phase

**Attack Overview**

Source code may have vulnerabilities during review; by injecting malicious code into the LLM application's source code and using vulnerabilities to hide it from review, an attacker poisons the source code of third-party open-source or commercial components, causing security issues in the application at training or runtime and affecting downstream model-application business developers who use these components.

**Attack Cases**

Case
Description




Case 1
An attacker can manipulate the model by uploading malicious code to open-source sites, thereby affecting domains such as investment, trading, and news

**Attack Risks**

Backdoor insertion: by injecting backdoor code into training data, an attacker can control or manipulate the model's output during inference, leading to unauthorized access or data manipulation.
Supply-chain attack: by injecting malicious code into open-source code, an attacker can affect the entire supply chain that uses it.
Fake-news propaganda: an attacker can use this technique to modify content such as movie reviews or news reports to spread misinformation or propaganda.

**Mitigations**

Mitigation
Description




Detect changes that deviate from the original code
Identify and block abnormal behavior caused by malicious code modification


Input validation and filtering
Strictly validate and sanitize code before it is fed into the model

**References**

https://drive.google.com/file/d/1CTVcliUblX35cWfB49Xjhf8xk-fM3QH1/edit?pli=1

---
### LLM-Application Source-Code Theft

> Risk ID: GAARM.0037
> Lifecycle: training phase

**Attack Overview**

This risk means the source code of the model or LLM is improperly stored, or the deployment environment has security risks, so unauthorized people may attack the deployment environment and steal the LLM application's source code, harming the enterprise's technical competitive advantage.

**Attack Cases**

Case
Description




Case 1
Meta's 65-billion-parameter language model was leaked


Case 2
A large amount of information about OpenAI's GPT-4—model architecture, training cost, datasets, and more—was leaked

**Attack Risks**

Loss of technical advantage: competitors may copy or modify leaked source code, weakening the enterprise's technical competitive advantage.
Cybersecurity threat: an attacker can use leaked source code to design targeted cyberattacks, for example penetrating the system through revealed vulnerabilities.
Phishing-email risk: leaked source code may be used to create more deceptive phishing emails that imitate the enterprise's internal applications, increasing the risk of users being deceived.

**Mitigations**

Mitigation
Description




Code-encryption protection
Use strong encryption to encrypt the LLM application's source code, preventing unauthorized access and leakage


Access-permission control
Restrict access to the LLM application's source code so only authorized personnel can view or modify it


Model monitoring
Monitor the model's usage to ensure it is not used for malicious purposes

**References**

https://analyticsindiamag.com/metas-llama-leaked-to-the-public-thanks-to-4chan/
https://knightcolumbia.org/blog/the-llama-is-out-of-the-bag-should-we-expect-a-tidal-wave-of-disinformation

---
## Training Phase

### Insecure Output Handling in LLM Applications

> Risk ID: GAARM.0035.003
> Lifecycle: training phase

**Attack Overview**

This risk arises when a downstream component accepts LLM output without proper review. The model's downstream components include various functional agents; lacking relevant output handling lets an attacker abuse the agents via the model to carry out attacks—for example, by inputting specific text to induce the LLM to output a response containing sensitive information and thereby steal user data, or directly output an unexpected attack payload, causing downstream vulnerabilities such as RCE and SSRF.

**Attack Cases**

Case
Description




Case 1
CVE-2023-29374 is an arbitrary-code-execution vulnerability in Langchain; programs using Langchain 0.0.131 or earlier and calling the Langchain LLMMathChain chain have a security risk of arbitrary command execution, potentially leaking sensitive information such as the OpenAI key and letting the Langchain server be controlled.


Case 2
Auto-GPT before v0.4.3 has a path-traversal vulnerability that lets arbitrary code run outside the Docker environment on the host running Auto-GPT. An attacker can use it for a targeted attack, endangering the site's system security

**Attack Risks**

Sensitive-information leakage: the LLM sometimes fails to sanitize JavaScript in its responses. An attacker may use a carefully designed prompt to make the LLM return a JavaScript payload; when the victim's browser parses it, they are attacked and sensitive information such as conversation history is leaked.
Arbitrary code execution: an attacker can execute arbitrary code via a vulnerability, potentially performing malicious operations on the server such as planting a backdoor, extracting sensitive data, or disrupting service.
Targeted

**Mitigations**

Mitigation
Description




Zero-trust framework
In this framework, every request to access a resource is treated as coming from an untrusted network, and the system inspects, authenticates, and verifies it to provide security


Sandbox environment
Try to run code in a sandbox for greater system security. For example, running code only in a dedicated ephemeral Docker container can significantly limit the potential impact of malicious code

**References**

https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf
https://cloud.baidu.com/article/3253170
https://www.akto.io/blog/insecure-output-handling-in-llms-insights
https://journal.hexmos.com/insecure-output-handling/
https://systemweakness.com/new-prompt-injection-attack-on-chatgpt-web-version-ef717492c5c2

---
### Traditional Vulnerability Risks in LLM Applications

> Risk ID: GAARM.0035.002
> Lifecycle: training phase

**Attack Overview**

Traditional application-security vulnerabilities exist not only in conventional software systems but also in LLM applications. For example, common API attacks, account takeover, and code execution still apply to LLMs, so best security practices must be strictly followed during the training phase to ensure the system has adequate defenses against traditional risks; otherwise it may lead to service disruption, account takeover, data tampering, and other dangers.

**Attack Cases**

Case
Description




Case 1
The case reports signs of ChatGPT being hit by a DDoS (distributed denial-of-service) attack, with external attackers trying to overload the network or server by repeatedly sending ping requests until it crashed


Case 2
The ChatGPT-Next-Web application has an SSRF vulnerability (CVE-2023-49785) that can be used to probe internal network resources

**Attack Risks**

Service disruption: a denial-of-service attack or resource exhaustion makes the LLM application unable to respond to user requests, affecting business continuity.
System control: a remote-code-execution or script-execution vulnerability may let an attacker take over the server, plant malware, or perform destructive operations.

**Mitigations**

Mitigation
Description




Strengthen API security
Ensure all API interfaces go through strict authentication and authorization control, restricting access.


Least-privilege principle
Limit or disable unnecessary command-execution features in the LLM application to reduce the potential attack surface.


Regular security assessment
Regularly scan the LLM application for security vulnerabilities and promptly patch what is found.

**References**

https://sec.cafe/handbook/security_research/ai_security/llm_security/attack/

---
### LLM Plugins: Insecure Input Handling

> Risk ID: GAARM.0035.001
> Lifecycle: training phase

**Attack Overview**

This risk means the LLM's plugins have insecure input handling that introduces risk into the model. For example, a plugin may take free-text input from the model without validation or type checking to handle context-size limits, letting a potential attacker craft a malicious request to the plugin, which may cause various undesired behaviors including remote code execution.

**Attack Cases**

Case
Description




Case 1
PALChain in LangChain was found to have a code-execution risk

**Attack Risks**

Unauthorized request execution: an attacker can directly exploit an LLM-application vulnerability, or manipulate the input prompt, to make the LLM application execute unexpected requests and access or operate restricted resources.
Sensitive-information leakage: accessing restricted resources through the LLM may lead to unauthorized acquisition and leakage of sensitive information.

**Mitigations**

Mitigation
Description




Input validation and filtering
Implement strict input-validation and sanitization so all input data is checked and cleaned before the LLM processes it


Least-privilege principle
Follow the least-privilege principle, granting the LLM only the minimum access needed for its task and avoiding excessive authorization

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/SSRF.html
https://www.horizon3.ai/attack-research/attack-blogs/nextchat-an-ai-chatbot-that-lets-you-talk-to-anyone-you-want-to/
https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf

---
### LLM Plugins: Excessive Agency

> Risk ID: GAARM.0036
> Lifecycle: training phase

**Attack Overview**

LLM-based systems are usually granted some business agency by developers—the ability to interact with other systems and perform actions in response to prompts. Excessive agency is a design/development-phase security risk that leads to destructive operations when the LLM produces unexpected or ambiguous output, usually rooted in too much functionality or too much autonomy. Excessive agency can cause a range of confidentiality, integrity, and availability impacts, depending on which systems the LLM application can interact with. For example, granting the LLM system excessive autonomy means that, when the LLM-based application or plugin fails to independently verify and approve high-impact operations, a plugin allowed to delete user documents performs the deletion without any user confirmation.

**Attack Cases**

Case
Description




Case 1
This video shows how to use an excessive-agency vulnerability to illegitimately reset a user's password

**Attack Risks**

Sensitive-information leakage: excessive agency may let the LLM, when maliciously manipulated, leak sensitive information and privacy.

**Mitigations**

Mitigation
Description




Least-privilege principle
Limit the plugins/tools an LLM agent is allowed to call to the minimum functionality needed. For example, if the LLM-based system does not need the ability to fetch URL content, such a plugin should not be provided to the LLM agent


Avoid open-ended capabilities
Where possible, avoid open-ended capabilities (such as running shell commands or fetching URLs) and use more fine-grained plugins/tools. For example, an LLM-based application may need to write some output to a file. Implementing this by running a shell command through a plugin makes the scope of undesired operations very large (any other shell command could run). A safer alternative is to build a file-writing plugin that only supports that specific function.

**References**

https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf

---
### RAG Development-Framework Vulnerabilities

> Risk ID: GAARM.0034.002
> Lifecycle: training phase

**Attack Overview**

RAG (Retrieval-Augmented Generation) is a framework combining information retrieval and generation, used in large-language-model development to enhance the model's generation. Because the RAG framework relies on the retrieval module to obtain information from external data sources, if the retrieval module's source data is inaccurate or unreliable, the generated answers may contain wrong or misleading information; and the various agents the framework introduces may also have security risks. RAG-related security risks center on the RAG generation module, retrieval module, integrated plugins, and external interfaces; insecure RAG design may introduce security vulnerabilities into the LLM application. For example, if the RAG retrieval module is designed to let the server make unrestricted requests, it may enable an SSRF vulnerability.

**Attack Cases**

Case
Description




Case 1
SSRF in the LangChain framework and RCE in PALChain bring security risks to LLM applications that use the framework

**Attack Risks**

Information disclosure: an attacker may use a path-traversal vulnerability to access sensitive files or system config files, leaking internal system information.
System control: if system files contain sensitive configuration information or scripts, an attacker may further use them to control the system.
Command execution: agents in the framework such as data-expression evaluation and the Python interpreter may be abused to cause an RCE attack.

**Mitigations**

Mitigation
Description




Input validation
Strictly validate and sanitize all user input to prevent path-traversal attacks.


Permission management
Set appropriate file permissions to prevent unauthorized file access.


Updates and fixes
Keep the application and its dependencies at the latest versions and promptly apply security patches to fix known vulnerabilities.

**References**

https://www.wehelpwin.com/article/5063
https://medium.com/nfactor-technologies/rag-poisoning-an-emerging-threat-in-ai-systems-660f9ff279f9
https://ironcorelabs.com/security-risks-rag/

---
### Insecure Coding Practices

> Risk ID: GAARM.0035
> Lifecycle: training phase

**Attack Overview**

Insecure coding practices refers to security issues caused by design flaws when developing LLM applications on top of a large-model integration framework. The code logic used in LLM-application development may introduce exploitable security vulnerabilities. These vulnerabilities fall into two broad categories:

LLM-application services have traditional vulnerabilities—for example, an externally facing chat system service may allow unauthorized viewing of others' conversation records;
New Tools, Agents, and Chains in the LLM integration framework contain security risks, letting an attacker indirectly exploit the related vulnerabilities through the LLM;

**Attack Cases**

Case
Description




Case 1
PALChain in LangChain was found to have a code-execution risk


Case 2
Multiple high-risk RCE vulnerabilities were discovered in LangChain

**Attack Risks**

Insecure coding practices: when generating code, the LLM may follow insecure coding practices, producing code that contains security vulnerabilities.
Unauthorized request execution: an attacker can directly exploit an LLM-application vulnerability, or manipulate the input prompt, to make the LLM application execute unexpected requests and access or operate restricted resources.

**Mitigations**

Mitigation
Description




Automated detection and evaluation
Use static-analysis tools to detect insecure patterns in code and improve code security


Least-privilege principle
Follow the least-privilege principle, granting the LLM only the minimum access needed to do its task and avoiding excessive agency


Input validation and filtering
Implement strict input-validation and sanitization so all input data is checked and cleaned before the LLM processes it

**References**

https://arxiv.org/html/2312.04724v1

---
### Data-Processing-Component Vulnerabilities

> Risk ID: GAARM.0034.001
> Lifecycle: training phase

**Attack Overview**

During AI-model development, dataset security is an important aspect that cannot be ignored. Platforms such as Hugging Face and GitHub may host datasets with malicious backdoors, which can threaten model security via the features or vulnerabilities of the LLM's data-processing components. When a developer trains on such a poisoned dataset, the hidden malicious code may execute, causing a series of security issues such as leakage or tampering of the model, dataset, and code.

**Attack Cases**

Case
Description




Case 1
Hugging Face's datasets component was found to have insecure behavior; loading a malicious dataset with it may cause risks such as command execution

**Attack Risks**

System intrusion: the attacker's crafted malicious script can connect to the attacker's server and execute system commands, controlling the victim's server.
Data leakage: a malicious script can steal sensitive data on the server such as training data and model code, leaking intellectual property and user privacy.
Model-parameter tampering: the model's parameters may be maliciously tampered with, affecting its accuracy and reliability.

**Mitigations**

Mitigation
Description




Trusted sources for training/fine-tuning datasets
Ensure the source dataset is trustworthy, check the dataset scripts for malicious Python code, and be cautious with datasets flagged as risky on Hugging Face


Large-model component supply-chain security protection
Continuously follow the latest supply-chain-security developments and recommendations in areas such as large-model native security, foundational security, and large-model-enabled R&D security

**References**

https://security.tencent.com/index.php/blog/msg/209

---
### Third-Party-Component Vulnerabilities

> Risk ID: GAARM.0034
> Lifecycle: training phase

**Attack Overview**

This attack refers to LLM-application developers possibly using third-party commercial or open-source library components during the training phase; these components may contain malicious code or vulnerabilities that can lead to compromise of the developer machine or server—a supply-chain security risk in the AI context.

**Attack Cases**

Case
Description




Case 1
The Python client redis-py for the Redis database uses an async interface; when a command is canceled, users' business data reads may become garbled (CVE-2023-28858)


Case 2
TorchServe can lead to unauthorized server access and achieve remote code execution on a vulnerable instance


Case 3
Hugging Face's datasets component has a vulnerability that allows attacks via a malicious dataset, potentially compromising the user's device and letting the model's parameters be stolen or tampered with


Case 4
This article studies the impact of backdoor attacks on pretrained models; an attacker can plant a backdoor to manipulate the model's recommendation results for malicious marketing or other purposes


Case 5
ChatGPT-Next-Web has SSRF and reflected-XSS vulnerabilities

**Attack Risks**

Supply-chain backdoor-poisoning attack: when an AI developer uses a third-party open-source library to load a dataset, if the dataset has malicious code planted in it, the PC or server may be attacked.
Model-parameter leakage or tampering: causing the model's parameters to be stolen or tampered with, affecting its security and reliability.

**Mitigations**

Mitigation
Description




Large-model component supply-chain security protection
For known vulnerabilities such as TorchServe's CVE-2023-43654, promptly update to a secure version


Trusted sources for training/fine-tuning datasets
Ensure the dataset source is trustworthy, check the dataset scripts for malicious Python code, and avoid using datasets flagged as risky on Hugging Face


Strictly control the introduction of open-source components
Establish an internal open-source governance system, strictly control the introduction of open-source components, and use tools for automated monitoring and tracking

**References**

https://hiddenlayer.com/research/insane-in-the-supply-chain/

---

---

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
