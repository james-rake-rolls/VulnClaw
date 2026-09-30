# AI Identity Security - Deployment Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-identity-security.md
> Phase: deployment phase (unauthorized access/credential abuse)

## Deployment Phase

### Public-Service API-Key Abuse

> Risk ID: GAARM.0049.001
> Lifecycle: deployment phase

**Attack Overview**

This risk means exposing the service's API access token (an authentication credential) through code, configuration, and the like, so an attacker may illegitimately gain access to the model-deployment environment, causing data leakage, model manipulation, and other security risks.

**Attack Cases**

Case
Description




Case 1
The AI-cybersecurity startup Lasso found over 1,600 Hugging Face API tokens leaked in code repositories, affecting hundreds of organizations' accounts

**Attack Risks**

Account compromise: a leaked API token may lead to unauthorized access to the company/organization account.
Data manipulation: an attacker controlling an account can manipulate an existing AI model and plant malicious code in it, affecting downstream users who rely on these base models.

**Mitigations**

Mitigation
Description




Strengthen authentication
Implement strengthened authentication measures such as multi-factor authentication to reduce the risk of API-token theft


Revoke leaked API tokens
Immediately revoke and replace any API tokens that may have been leaked


Key-management and rotation mechanisms
Establish secure key-management and rotation mechanisms and regularly rotate API tokens.


**References**

- https://www.securityweek.com/major-organizations-using-hugging-face-ai-tools-put-at-risk-by-leaked-api-tokens/
- https://aws.amazon.com/cn/what-is/api-key/

---
### Vector-Database Unauthorized Access

> Risk ID: GAARM.0050
> Lifecycle: deployment phase

**Attack Overview**

During RAG application development, various local documents are split by a Text class into shorter passages, an embedding model vectorizes the text content, and it is finally stored in a vector database. By accessing the database without authorization, an attacker tampers with and corrupts the model, further affecting the RAG system's inaccurate or malicious retrieval, which may affect the RAG system's output and pose an indirect-prompt-injection risk.

  

RAG application-architecture forms

**Attack Cases**

Case
Description




Case 1
anything-llm has vulnerability CVE-2024-0551, which lets an unauthenticated attacker download files from the database


Case 2
This research proposes a new attack against RAG-augmented LLMs that compromises the victim's RAG system by injecting a single malicious document into its knowledge database, enabling several malicious attacks against the generative model.

**Attack Risks**

Vector-database corruption: unauthorized changes can corrupt the knowledge source, causing the RAG system to retrieve inaccurate or malicious content.
Information disclosure: sensitive information stored in the vector database is leaked.
Indirect-prompt-injection risk: an attack against the availability of a vector database may affect the RAG systems that depend on it.

**Mitigations**

Mitigation
Description




Data encryption
Encrypt the vector database that stores all index and embedding data to protect it from potential leakage or unauthorized access


Authentication and access control
Use strong user authentication and authorization to ensure only authorized personnel can access the database


Backup and redundant storage
Regular backups ensure the knowledge source can be restored if data is corrupted or lost


Security updates and auditing
Regularly update and audit the vector-database system to fix vulnerabilities and strengthen security

**References**

https://medium.com/@nitishjoshi060291/llm-hallucinations-fix-it-with-vector-database-de04eee531da
https://cloudsecurityalliance.org/blog/2023/11/22/mitigating-security-risks-in-retrieval-augmented-generation-rag-llm-applications
https://www.cnblogs.com/LittleHann/p/17440063.html#_label3
https://dongnian.icu/llms/llms_article/9.%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BALLM/index.html
https://cloudsecurityalliance.org/blog/2023/11/22/mitigating-security-risks-in-retrieval-augmented-generation-rag-llm-applications

---
### Unauthorized Access to the Model-Deployment Environment

> Risk ID: GAARM.0051
> Lifecycle: deployment phase

**Attack Overview**

This risk means an attacker exploits risks in the ML deployment-platform service—such as misconfiguration, known vulnerabilities, or lack of proper authentication and authorization—to gain unauthorized access to the ML deployment environment and then steal sensitive data, abuse compute resources, undermine the AI model's integrity, or conduct other malicious activity.

**Attack Cases**

Case
Description




Case 1
An attacker exploited an API unauthorized-access risk in the Ray framework to achieve remote code execution and gain control of the target enterprise's compute resources

**Attack Risks**

Sensitive-information leakage: an attacker may access and steal sensitive information such as training data, model parameters, and user data.
Malicious operation: unauthorized access may let the model be maliciously operated, producing misleading output.
Resource abuse: an attacker may use the compute resources of the ML deployment environment without authorization for mining or other compute-intensive tasks.
Model-integrity damage: an attacker may modify or poison the AI model's training process, lowering its accuracy or producing misleading results.
Service disruption: the attacker's actions may cause an ML-service outage, affecting business continuity.

**Mitigations**

Mitigation
Description




Strengthen authentication and access control
Implement access-control and authentication mechanisms to prevent unauthorized access to the LLM deployment-platform environment and its data, and avoid using the ML platform service's default authentication policy


Regular updates and patching
Promptly update the ML platform and dependent libraries to fix known vulnerabilities


Model protection and secure deployment
Security-scan and penetration-test the model before deployment, and use techniques such as encryption and signing to protect the confidentiality and integrity of the model's parameters and training data

**References**

https://www.leewayhertz.com/security-in-ai-development/

---
### Abusing Deployment-Environment Credentials

> Risk ID: GAARM.0049
> Lifecycle: deployment phase

**Attack Overview**

In the large-model MLOps lifecycle, access credentials (such as keys or access tokens) are involved across the commit, build, test, and deploy stages. The risk of abusing deployment-environment credentials means that the use of API keys or access tokens for accessing and deploying the model service in the large-model CI/CD pipeline has security weaknesses, which an attacker can exploit to steal credentials, inject malicious code, and cause sensitive-information leakage, malicious-code injection, or other security threats.

**Attack Cases**

Case
Description




Case 1
Credentials hardcoded in code or config files let an attacker, after gaining access to a developer machine, use them for lateral movement

**Attack Risks**

Credential leakage: an attacker obtains a developer's credentials via social engineering or other means, then uses them to access sensitive data in the CI/CD system or perform malicious operations.
Malicious-code injection: using obtained credentials, an attacker commits malicious code to the repository, which is executed during subsequent build and deployment.

**Mitigations**

Mitigation
Description




Strengthen authentication and password policies
Advise users to follow proper password policies and use two-factor authentication (2FA)


Code audit and automated scanning
Run automated security scans before code commit and deployment to detect hardcoded-credential risks and surface potential security issues


Monitoring and alerting
Deploy a monitoring system to detect unusual access patterns or operations and alert promptly

**References**

https://atmosphericthinking.medium.com/massive-leak-of-chatgpt-credentials-over-100-000-affected-db6cef3a18c5
https://blog.csdn.net/FreeBuf_/article/details/140870185?utm_relevant_index=7

---
