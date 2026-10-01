# AI Identity Security - Training Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-identity-security.md
> Phase: training phase (permission-design flaws/environment authentication)

## Training Phase

### LLM Plugins: Permission-Control Design Flaws

> Risk ID: GAARM.0048
> Lifecycle: training phase

**Attack Overview**

This risk refers to a permission-control design flaw in LLM plugins. An LLM plugin is an agent that provides interactive functionality and, when enabled, is automatically called by the model during user interaction. Such automatic calling carries an uncontrolled risk—for example one plugin may use another plugin's permissions to access sensitive data or functions it cannot directly access, giving an attacker the chance to craft malicious requests. In short, this flawed access control lets users directly schedule sensitive-function plugins, or there is wrong permission control between plugins, so that when the end user supplies malicious input, security risks arise including data leakage, remote code execution, and privilege escalation.

**Attack Cases**

Case
Description




Case 1
LangChain provides many tools for building LLM plugins; when these plugins are not designed with security as the top priority, an attacker can use prompt injection to subvert the behavior of a poorly designed plugin

**Attack Risks**

Sensitive-information leakage: a plugin with poorly designed permission control may, after being invoked by an attacker, request another plugin's permissions to access its data or functions; such chained invocation may leak much sensitive information.
Remote code execution: by injecting malicious code or data, an attacker may try to gain a foothold in the system to further control or damage it.

**Mitigations**

Mitigation
Description




Enforce strict parameterized input
Perform type and range checks on input. If that is not possible, introduce a second typed layer that parses the request and applies validation and sanitization


Least-privilege access control
Expose as little functionality as possible while still performing the required function

**References**

https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf
https://developer.nvidia.com/zh-cn/blog/securing-llm-systems-against-prompt-injection/

---
### Training Environment Lacking Authentication/Authorization

> Risk ID: GAARM.0046
> Lifecycle: training phase

**Attack Overview**

This risk means the model's training phase lacks strict access control and authentication, so resources such as the internal training data, training infrastructure, and training framework can be accessed by under-privileged people, leaking the model's sensitive data, making the training data transparent, and increasing the risk of model poisoning.

**Attack Cases**

Case
Description




Case 1
In the ShadowRay incident, the attacker exploited CVE-2023-48022 in the Ray framework, scheduling the Jobs API without authorization to achieve an RCE attack

**Attack Risks**

Sensitive-information leakage: unauthorized access to training data leads to sensitive-information leakage.
Degraded model quality: maliciously tampering with training data may affect the model's learning, causing inaccurate or biased output.
High-value resource abuse: an attacker uses unauthorized API access to control high-value compute resources and conduct activities such as cryptocurrency mining.

**Mitigations**

Mitigation
Description




Strengthen authentication and access-control policies
Implement access-control and authentication mechanisms to prevent unauthorized access to the LLM training environment and its data


Data encryption and desensitization
Introduce encryption and privacy-protection measures for training data to prevent sensitive-information leakage

**References**

https://blog.csdn.net/qq_43543209/article/details/135683986

---
### Excessive Privilege Allocation in the Training Environment

> Risk ID: GAARM.0047
> Lifecycle: training phase

**Attack Overview**

The risk of excessive privilege allocation during large-model training mainly concerns security issues caused by over-broad privileges in data access, model training, and system administration, which may lead to unauthorized access or abuse. If an attacker illegitimately gains a developer's control privileges, they may use these excessive privileges to illegitimately access, tamper with, or destroy the model's training data, affecting the model's quality and security.

**Attack Cases**

Case
Description




Case 1
Via phishing or other means, an attacker obtains a training developer's control privileges and uses the high-privilege account credentials to access sensitive training data or maliciously tamper with the model

**Attack Risks**

Sensitive-data leakage: if a developer's training environment has excessive, unnecessary privileges, then when the developer's credentials are leaked, an attacker may use the redundant privileges to access more internal information, potentially leaking training data, especially when it contains sensitive information.
Degraded model quality: an attacker maliciously tampering with training data may affect the model's learning, causing inaccurate or biased output.

**Mitigations**

Mitigation
Description




Least-privilege principle
Ensure each user or system component has only the minimum privileges needed for its task


Data encryption and desensitization
Introduce encryption and privacy-protection measures for training data to prevent sensitive-information leakage


Access control and auditing
Implement strict access-control policies and conduct regular security audits to monitor and log all access to data and models

**References**

https://www.pulumi.com/ai/answers/mptvxaHguJ6A4yXSHi92zZ/implementing-role-based-access-to-ai-training-data-in-snowflake

---
