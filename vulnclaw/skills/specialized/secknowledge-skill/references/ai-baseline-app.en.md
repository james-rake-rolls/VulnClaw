# AI Foundation Security - Application Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-baseline-security.md
> Phase: application phase (container escape/denial of service/code-execution escape)

## Application Phase

### LLM Denial of Service and Resource Exhaustion

> Risk ID: GAARM.0008
> Lifecycle: application phase

**Attack Overview**

An attacker may send a large number of requests to attack the ML system, slowing the ML service or forcing it to shut down. Since LLM systems require large amounts of dedicated compute, an attacker can deliberately craft inputs requiring large amounts of useless computation to consume the LLM system's resources, degrading service quality for the LLM and other users and potentially incurring high resource costs. Because of the LLM's resource-intensive nature and the unpredictability of user input, the harm of this vulnerability is easily amplified.

**Attack Cases**

Case
Description




Case 1
Perform prompt injection in the agent to trick it into repeatedly calling the LLM and SerpAPI, rapidly increasing costs.


Case 2
Because a Sourcegraph site-admin access token was accidentally leaked and used to impersonate a user to gain access to the system admin console, API usage rose significantly and a large amount of user data was leaked.


Case 3
Use prompt injection to make MathGPT leak its API key and cause a denial of service


Case 4
Using an LLM for decision-making in a power system: a DoS attack could delay or corrupt decisions, ultimately affecting the power system's stable operation

**Attack Risks**

Resource-exhaustion attack: an attacker may send a large number of requests to occupy the model's compute resources, making the service unavailable, degrading user experience, and even causing an outage.
Data leakage and abuse: the attack may cause the model to anomalously leak sensitive information such as API tokens, which the attacker may use for unauthorized access.

**Mitigations**

Mitigation
Description




API rate limiting
Enforce API rate limits, restricting how many requests an individual user or IP can make in a given period


Limit the number of executions
Limit the number of queued operations and the total number of operations in systems that respond to the LLM


Real-time monitoring and alerting
Continuously monitor hardware resource utilization to identify abnormal spikes or patterns that may indicate a denial-of-service attack

**References**

https://atlas.mitre.org/techniques/AML.T0029
https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-2023-v05.pdf
https://www.cnblogs.com/LittleHann/p/17596696.html

---
### Code-Interpreter Execution Escape

> Risk ID: GAARM.0007.001
> Lifecycle: application phase

**Attack Overview**

This risk means an attacker uses the code-interpreter capabilities of models such as GPT-4—its ability to parse and generate code—to gradually build and hide malicious code across multiple conversational-context interactions, using Unicode characters and encoding obfuscation, thereby hiding and bypassing the malicious code, defeating the model application's code-safety-check mechanism, completing a sandbox escape, and gaining access to the system. Such malicious code is highly stealthy and hard to detect; once the sandbox isolation is broken, the attacker can control the whole system, steal data, plant backdoors, and more.

**Attack Cases**

Case
Description




Case 1
While GPT-4 executed code, the attacker hid and bypassed the malicious code through multiple conversational-context interactions and encoding, finally triggering execution via a string, bypassing GPT-4's safety checks, running the cat /etc/issue command, and successfully learning the target environment's Linux distribution

**Attack Risks**

Data-leakage risk: an attacker can extract sensitive data from the LLM application or its connected systems.
System-integrity risk: an attacker can perform unauthorized operations, modify system settings or files, and even plant malicious code, damaging the system.
Privilege-escalation risk: once an attacker escapes the sandbox, they may gain higher-privilege access than they originally had.

**Mitigations**

Mitigation
Description




Rigorously test the isolation environment
Rigorously test and validate the sandbox to ensure it is secure


Input/output validation
Filter out unsafe prompts to maximize system security


Access control
Implement strict access control and privilege separation in the LLM application and its sandbox so that only authorized entities can access sensitive resources, and restrict privileged operations

**References**

https://blog.securelayer7.net/owasp-top10-for-large-language-models/
https://www.mufeedvh.com/llm-security/#2-sandboxing-extended-llms
https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_Sandboxing.html

---
### Container-Runtime Risks

> Risk ID: GAARM.0004 (inferred from the AISS taxonomy)
> Lifecycle: deployment phase

**Attack Overview**

LLM applications built on an integration framework usually combine a K8s cluster and container environment to build and isolate each agent's runtime. By crafting prompts, an attacker can indirectly have the model's agent perform attacks against the container-runtime environment, achieving container escape, container privilege escalation, and similar attacks.

**Attack Cases**

Case
Description




Case 1
Wiz obtained container-runtime privileges of a model by uploading a malicious model to Hugging Face.

**Attack Risks**

Breaking container isolation: by exploiting a container vulnerability or configuration flaw, an attacker tries to break the container's isolation and gain access to the host.
Image-content tampering: an attacker may tamper with the model image's content and plant malicious code.
Data leakage: an attacker may obtain sensitive data such as filesystem information on the host.
Service disruption: an attacker may disrupt services on the host, making them unavailable.
Lateral movement: an attacker may use the escaped container as a pivot to further attack other systems on the internal network.
Persistent control: an attacker may install a backdoor on the host for long-term control.

**Mitigations**

Mitigation
Description




Periodic review
Regularly scan container images and dependency components to ensure there are no security vulnerabilities.


Resource limits and access isolation
Implement resource limits and isolation to prevent a single container from consuming excessive resources and affecting other machines in the cluster.


Least-privilege principle
Avoid running privileged containers with modes such as --privileged; grant containers only the minimum permission set they need.


Input/output validation
Ensure the safety of prompts and results on both the input and output sides of the model, and block suspicious attack behavior

**References**

https://mp.weixin.qq.com/s/tf4ljSJ0Ue0YniojWhYMKg
https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure

---
### Container-Cluster Environment Probing

> Risk ID: GAARM.0006
> Lifecycle: application phase

**Attack Overview**

This risk means an attacker exploits security issues in the model's deployment environment—the third-party cloud vendor or a self-built K8s cluster—such as system-privilege control, misconfiguration, the cluster's own vulnerabilities, or third-party integration plugins. They attack features such as the agents in the LLM integrated application, using those features' interaction with the business deployment environment to attack the model's business-application system. After successfully penetrating the deployment environment, risks such as sensitive-data leakage and backdoor implantation may result.

**Attack Cases**

Case
Description




Case 1
Wiz obtained runtime privileges of a model by uploading a malicious model to Hugging Face, then used an EKS-cluster misconfiguration to achieve privilege escalation.

**Attack Risks**

Resource-exhaustion attack: unrestricted access to resources may become an attack vector, letting an attacker consume large amounts of resources and affect the system's normal operation.
Privileged-mode runtime risk: a container running in privileged mode may increase the risk of system compromise.
Unauthorized cluster access: if no security measures are in place or the cluster is misconfigured, an attacker may gain full access to the entire cluster.

**Mitigations**

Mitigation
Description




Periodic review
Regularly scan container images and dependency components to ensure there are no security vulnerabilities


Resource limits and access isolation
Implement resource limits and isolation to prevent a single container from consuming excessive resources, and restrict resource access via secrets and specific permission roles created in Kubernetes


Control network traffic
Use Kubernetes network policies to control inbound and outbound traffic between Pods, reducing potential intra-cluster lateral movement and

**References**

https://pradiptabanerjee.medium.com/confidential-containers-for-large-language-models-42477436345a


https://www.run.ai/guides/kubernetes-architecture/securing-your-ai-ml-kubernetes-environment

---
### Container-Cluster Environment Attacks

> Risk ID: GAARM.0007
> Lifecycle: application phase

**Attack Overview**

LLM applications built on an integration framework usually integrate various functional agents deployed in the container environment of a Kubernetes cluster. By crafting prompts, an attacker can indirectly induce the LLM's agent to run container-probing commands, probing and collecting information about the cluster environment as reconnaissance for later attacks. After probing and collecting the information, they can target and exploit vulnerabilities and misconfigurations in the cluster to further penetrate and attack the entire container cluster.

**Attack Cases**

Case
Description




Case 1
While GPT-4 executed code, the attacker hid and bypassed the malicious code through multiple conversational-context interactions and encoding, finally triggering execution via a string, bypassing GPT-4's safety checks, running the cat /etc/issue command, and successfully obtaining the target environment's Linux distribution and cluster environment variables

**Attack Risks**

Cluster-environment information disclosure: by crafting specific prompts, an attacker may induce the AI model to execute unauthorized commands and leak the container's internal architecture or security-configuration information.
Cluster security-configuration leakage: through probing an attacker can obtain the cluster's security-configuration details, lowering the cluster's security and increasing the risk of compromise.

**Mitigations**

Mitigation
Description




Implement strict access control
Ensure all services and ports are strictly reviewed, authorizing only necessary access to reduce the potential attack surface


Input/output validation
Ensure the safety of prompts and results on both the input and output sides of the model, and block suspicious attack behavior

**References**

https://mp.weixin.qq.com/s/Ry1PoZLfPvw6Lj8bz14mgw

---
