# AI Application Security - Training Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-app-security.md
> Phase: training phase (GAARM.0034-0036 third-party components/plugins/insecure code)

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

