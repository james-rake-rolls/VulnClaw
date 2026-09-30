# AI Application Security - Deployment Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-app-security.md
> Phase: deployment phase (GAARM.0037-0038, 0049 API management/source-code poisoning/theft)

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
