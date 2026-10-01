# AI Foundation Security - Training Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-baseline-security.md
> Phase: training phase (development-tool vulnerabilities/environment isolation)

## Training Phase

### Model-Development-Tool Vulnerabilities

> Risk ID: GAARM.0001.001
> Lifecycle: training phase

**Attack Overview**

Model development and training involve multiple steps such as data preprocessing, feature engineering, model selection, training, evaluation, and deployment. If the tools used in this process have security vulnerabilities, the entire ML pipeline is at risk. An attacker can exploit them to tamper with training data, steal model parameters, or launch a specific attack after deployment, causing serious consequences such as inaccurate output, stolen parameters, and malware propagation.

**Attack Cases**

Case
Description




Case 1
TensorFlow has a code-execution vulnerability posing a code-execution risk when loading a model


Case 2
PyTorch has a code-execution vulnerability that can execute remote code on the target system in the context of the user running the program, posing a risk of executing malicious code


Case 3
This document covers different TensorFlow use cases and outlines its security-vulnerability issues, where different use cases bring different risk consequences

**Attack Risks**

Supply-chain attack: an attacker can plant malicious code in a legitimate software package used for ML development, carrying out a dependency-chain attack to spread malware during distribution.
Model poisoning: an attacker injects malicious data into the training data, affecting the model's decision process and causing inaccurate output or bias.
Intellectual-property loss: if the model's parameters are stolen, an attacker may copy or illegitimately use the model.

**Mitigations**

Mitigation
Description




Regular updates and patching
Keep all development tools and libraries up to date to benefit from the latest security fixes


A secure dependency chain
Review the dependency chain to ensure all third-party libraries and packages come from trusted sources

**References**

https://www.secrss.com/articles/64006
https://huntr.com/bounties/a795bf93-c91e-4c79-aae8-f7d8bda92e2a

---
### Training-Data-Management-System Vulnerabilities

> Risk ID: GAARM.0001.002
> Lifecycle: training phase

**Attack Overview**

The training-data-management system is responsible for storing, processing, labeling, and providing data, delivering prepared data to the model for learning. When this system has supply-chain-related vulnerabilities, an attacker can exploit them to tamper with or steal data, or even affect the model's training results through data poisoning.

**Attack Risks**

Data-poisoning attack: an attacker may inject malicious data into the training data, affecting the model's decision process and causing inaccurate predictions or bias.
Model-stealing attack: an attacker tries to reverse-engineer the model by querying it to obtain its parameters or training data, stealing intellectual property.
Data leakage: an attacker obtains sensitive training data through unauthorized access.

**Mitigations**

Mitigation
Description




Security updates and auditing
Regularly update and audit the training-data-management system to fix vulnerabilities and strengthen security


Monitoring and logs
Implement real-time monitoring and logging to promptly detect and respond to suspicious activity

**References**

https://doc.dataiku.com/dss/latest/concepts/homepage/index.html
https://www.secrss.com/articles/62742

---
### Training-Environment Security Risks

> Risk ID: GAARM.0001
> Lifecycle: training phase

**Attack Overview**

This risk means that the deep-learning frameworks (such as TensorFlow or PyTorch) and necessary dependency libraries used in the model's training and development environment—application-development components—may themselves have vulnerabilities that cause a supply-chain attack on downstream LLM applications, affecting the integrity of the training data, ML model, and deployment platform.

**Attack Cases**

Case
Description




Case 1
The integration-plugin sample code OpenAI provided included a vulnerable MinIO Docker image that could leak secrets and passwords; the redis-py library used by ChatGPT had a vulnerability that leaked users' chat history and payment information


Case 2
The open-source ML framework PyTorch has a major layer-level vulnerability CVE-2024-5480, which an attacker can use to remotely attack the master node of distributed training; once these nodes are compromised, the attacker may steal AI-related sensitive data


Case 3
The pickle format used by PyTorch models can be weaponized by threat actors to execute arbitrary code and deploy Cobalt Strike, Mythic, and Metasploit payloads; an attacker can use a malicious PyTorch binary to compromise a hosted conversion service and the file-hosting system

**Attack Risks**

User-privacy leakage: as shown in Case 1, due to a bug in the redis-py library, ChatGPT users' chat-record titles and conversation content could be seen by other users, leaking user privacy data.
System-integrity compromise: an attacker may use a vulnerability to damage system integrity, affecting the reliability and availability of the LLM service.

**Mitigations**

Mitigation
Description




Security updates and auditing
Regularly update and audit the service software in the training and development environment to fix vulnerabilities and strengthen security


Security auditing and monitoring
Conduct regular security audits, use monitoring tools to detect and alert on suspicious behavior, and keep effective logs

**References**

https://llmtop10.com/llm05/

---
### Training-Environment Isolation Flaws

> Risk ID: GAARM.0002
> Lifecycle: training phase

**Attack Overview**

Training-environment isolation means dividing the debug and runtime environments into two completely isolated zones to prevent the debug environment from penetrating the runtime environment. In the debug environment, program logic can be modified but only desensitized data may be used; in the runtime environment, the real full dataset can be operated on, operations are reviewed, and results are traceable and accountable. If training-environment isolation is flawed so one can move from the development environment into the runtime/test environment, unauthorized users can access sensitive data, giving an attacker an opening.

**Attack Cases**

Case
Description




Case 1
A training-environment isolation flaw lets an attacker move from the developer environment into the runtime/test environment, causing risks such as training-data leakage

**Attack Risks**

Data leakage: an attacker may access and steal sensitive data stored in the runtime environment, whose leakage may cause major financial loss and legal liability.
Gaining system control: if an attacker penetrates the runtime environment, they may gain system control and then manipulate data access, resource management, and system settings.

**Mitigations**

Mitigation
Description




Strengthen isolation measures
Use security techniques and best practices to strengthen isolation between the debug and runtime environments


Access control
Implement role-based access control (RBAC) so that only authorized personnel can access the runtime environment


Secure-sandbox technology
Isolate and protect the LLM's runtime environment to prevent external attacks and interference


**References**

- https://cloud.baidu.com/article/621826

---

