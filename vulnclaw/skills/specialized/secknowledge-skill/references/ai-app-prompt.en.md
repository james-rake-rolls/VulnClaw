# AI Application Security - Application Phase - Prompt Injection and Variants

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-app-app.md
> Risk category: prompt injection (GAARM.0039 direct injection / 0040.x indirect/XSS/Memory/worm / 0043.x keyword and synonym obfuscation / 0044 adversarial encoding / 0045 reverse induction / 0061 multimodal injection)

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
