# AI Application Security - Application Phase - Agent and CoT Attacks

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-app-app.md
> Risk category: Agent/CoT (GAARM.0041.x agent abuse and SSRF/RCE / 0042.x CoT injection and chain-of-thought interference / 0047 environment injection / 0056.001 query injection / 0060 unexpected code execution)

---

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
