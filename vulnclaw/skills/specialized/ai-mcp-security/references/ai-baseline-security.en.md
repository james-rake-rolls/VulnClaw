# AI Foundation Security

> Source: AISS NSFOCUS Large-Model Security Zhilian Community
> Entries: 19

---

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
## Deployment Phase

### CI/CD Pipeline Attacks

> Risk ID: GAARM.0004
> Lifecycle: deployment phase

**Attack Overview**

Across the full large-model development lifecycle, the CI/CD pipeline is responsible for pushing the model from development to production, automating LLM deployment, and handling subsequent updates and maintenance. A CI/CD-pipeline attack means that, while CI/CD pushes the model to production, vulnerabilities in the CI/CD infrastructure or unreliable third-party tools let an attacker attack the pipeline—for example by committing malicious code or poisoning dependencies—causing serious consequences such as illegitimate model tampering and sensitive-information leakage.

  

The CI/CD pipeline in the large-model development lifecycle

**Attack Cases**

Case
Description




Case 1
Use phishing to obtain a developer's or operator's credentials and then commit malicious code in the CI/CD pipeline.


Case 2
Exploit server vulnerabilities such as those in CI/CD infrastructure like GitLab and Jenkins.


Case 3
Attacking third-party tool and application dependencies, such as poisoning dependency packages or uploading a malicious package to a central open-source registry with a forged dependency name.

**Attack Risks**

Virtual-environment poisoning: the virtual environment or container in the CI environment is attacked, and the attacker may tamper with its dependencies or runtime configuration to affect model-training and deployment results.
Build-and-deploy pipeline tampering: an attacker may try to modify the automated build-and-deploy pipeline to insert malicious code or operations during model deployment.
Sensitive-information leakage: the CI/CD environment stores sensitive information (access credentials, config files, keys, etc.) that, if obtained by an attacker, may lead to sensitive-information leakage and privacy risk.
Denial-of-service attack: an attacker may use a DoS attack to make the CI/CD system malfunction, interrupting or delaying model development and deployment.
Unauthorized model access: the model-deployment process is attacked, and the attacker may use a vulnerability to gain unauthorized access and illegitimately operate on or tamper with the model.

**Mitigations**

Mitigation
Description




Strengthen access control and permission management
Restrict access to the CI/CD system and related environments so only authorized personnel can access critical resources


Security updates and auditing
Regularly update and audit the model-deployment software to fix vulnerabilities and strengthen security


Strengthen monitoring and logging
Promptly detect abnormal activity and attack behavior and respond quickly to reduce potential risk and loss

**References**

https://github.com/knownsec/KCon/blob/master/2023/CICD%E6%94%BB%E5%87%BB%E5%9C%BA%E6%99%AF.pdf

---
### Cloud-Platform Multi-Tenant Isolation Failure

> Risk ID: GAARM.0003.001
> Lifecycle: deployment phase

**Attack Overview**

In a multi-tenant cloud platform, each tenant should have an independent operating environment and data storage to ensure isolation of user behavior and data. Isolation failures may arise from design flaws or misconfiguration; as high-value compute services proliferate, an attacker may break tenant boundaries to access and tamper with other tenants' data or even perform malicious operations, so that data and resources between tenants (users or organizations) are not effectively protected, causing a series of security issues.

**Attack Cases**

Case
Description




Case 1
This article studies whether AI models run in an isolated environment; Wiz used the AWS IMDS metadata service to complete an Amazon EKS privilege escalation, took over the entire cluster service, moved laterally within the EKS cluster, and could further perform cross-tenant access, leading to sensitive-data leakage

**Attack Risks**

Data leakage: multi-tenant isolation failure may cause data confusion or leakage between tenants, potentially including sensitive information or personally identifiable information.
Reduced trust: a security incident can weaken user trust in the cloud-service provider.

**Mitigations**

Mitigation
Description




Strengthen access control
Strengthen access control over system resources through permission-control mechanisms such as access-control lists (ACLs) and role-based access control (RBAC)


Resource monitoring
Monitor resource usage to promptly detect abnormal behavior such as resource preemption or abuse

**References**

https://xie.infoq.cn/article/536a3e7e776eb32b38d1a9747
https://www.helloaliyun.com/tutorial/1039.html
https://support.huaweicloud.com/usermanual-gaussdbformysql/gaussdbformysql_05_0347.html

---
### Cloud-Platform Security Vulnerabilities

> Risk ID: GAARM.005
> Lifecycle: deployment phase

**Attack Overview**

Because large-model applications demand heavy compute, they usually rely on a cloud-platform environment for training and inference, so cloud-platform security is vital to large-model security. But security weaknesses caused by the cloud platform's technical defects, vulnerabilities, or lack of multi-factor authentication let an attacker maliciously attack the cloud-deployed model—for example reading sensitive data or illegitimately stealing and using account credentials—causing a range of losses including but not limited to data leakage, service disruption, and malicious code execution. These attacks affect not only the model's security but potentially other users of the cloud service.

**Attack Cases**

Case
Description




Case 1
A CSRF vulnerability was found in the Amazon SageMaker Notebook service, which an attacker could use to read sensitive data and perform arbitrary operations in the customer's environment


Case 2
Because a system on a vulnerable Laravel version (CVE-2021-3129) had security weaknesses, an attacker used AWS credentials stolen from Laravel to illegitimately probe which cloud-hosted model services the credentials could use, with the victim losing over $46,000 per day

**Attack Risks**

Data leakage: due to cloud-application vulnerabilities, insecure APIs, and similar causes, sensitive information may be accessed or disclosed by an unauthorized third party, causing serious privacy and compliance problems.
Unauthorized access to the model application: a cloud-platform vulnerability may expose the user's deployed model application to unauthorized-access risk.

**Mitigations**

Mitigation
Description




Strict access control
Ensure only authenticated and authorized users can access API endpoints


Least-privilege principle
Enforce the least-privilege principle so users and processes have only the access needed for their tasks

**References**

https://developer.aliyun.com/article/1430094

---
### Abusing Insecure System Configuration

> Risk ID: GAARM.0003
> Lifecycle: deployment phase

**Attack Overview**

This risk means that in the infrastructure environment where the model is deployed, an attacker exploits a series of insecure system configurations in the ML model-deployment system, deployment-cluster environment, deployment-container environment, and image-push management environment to carry out various attacks against the model's foundation environment.


Unauthorized access: misconfiguration may expose sensitive ports or weaken authentication, letting unauthorized users access system resources;


Container-security risk: an insecure container configuration may include unnecessary privileges, sensitive-file mounts, or container-escape vulnerabilities;


Cluster-security risk: in clusters such as Kubernetes, improper RBAC configuration may lead to privilege-escalation or lateral-movement attacks;


Image-security risk: insecure system configuration causes risks such as leakage of the image during transmission, management, and deployment;


Environment-isolation risk: misconfiguration may cause isolation to fail, letting an attacker access or affect other containers or the host;

**Attack Cases**

Case
Description




Case 1
ShadowRay: the first known attack campaign actively exploiting AI workloads in the wild

**Attack Risks**

Malicious operation: if the system is misconfigured, an attacker may exploit the vulnerabilities to gain access and then perform malicious operations.
Data leakage: an attacker may obtain sensitive data such as filesystem information on the host or secrets within the cluster.
Service disruption: an attacker may disrupt host or cluster services, making them unavailable.
Lateral movement: an attacker may use the escaped container or an escalated node as a pivot to further attack other systems on the internal network.
Persistent control: an attacker may install a backdoor on the host or in the cluster for long-term control.

**Mitigations**

Mitigation
Description




Least-privilege principle
Ensure container and cluster components have only the minimum privileges needed for their tasks


Ensure a secure system configuration
Avoid privileged containers, configure RBAC reasonably, and restrict access to the API server to avoid unnecessary risk exposure


Regular updates and patch management
Promptly update container and cluster components and apply security patches to reduce exploitation risk

**References**

https://pradiptabanerjee.medium.com/confidential-containers-for-large-language-models-42477436345a

---
### Vector-Database Vulnerabilities

> Risk ID: GAARM.0005 (sub-risk 1, parent: deployment-environment component supply-chain vulnerabilities)
> Lifecycle: deployment phase

**Attack Overview**

During RAG application development, various local documents are split by a Text class into shorter passages, an embedding model vectorizes the text content, and it is finally stored in a vector database. The vector database plays an important role in the RAG architecture, especially in handling high-dimensional data and performing approximate-nearest-neighbor (ANN) queries. Because of the vector database's importance, if it has vulnerabilities, an attacker can exploit them to gain unauthorized data access, tamper with data, execute malicious code, or launch other attacks, achieving goals such as obtaining sensitive information and remotely controlling malicious code, causing data loss.

**Attack Cases**

Case
Description




Case 1
Use the Qdrant vector-database API to achieve path traversal followed by file upload, leading to a remote-code-execution risk


Case 2
anything-llm has vulnerability CVE-2024-0551, which lets an unauthenticated attacker download files from the database


Case 3
This research proposes a new attack against RAG-augmented LLMs that compromises the victim's RAG system by injecting a single malicious document into its knowledge database, enabling several malicious attacks against the generative model.

**Attack Risks**

Data tampering: an attacker uses a vector-database vulnerability to tamper with embedding vectors, corrupting the data in the database and affecting its integrity.
User-privacy violation: the vector database may store sensitive information such as personal identity; if obtained by an attacker, it seriously violates user privacy.

**Mitigations**

Mitigation
Description




Regularly apply patches
Stay aware of the latest patches from the vector-database provider; regularly updating the database software ensures protection against known vulnerabilities


Data backup
Back up data regularly so it can be quickly restored if tampered with


Monitoring and logs
Implement real-time monitoring and logging to promptly detect and respond to suspicious activity

**References**

https://ironcorelabs.com/security-risks-rag/

---
### Container and Cluster System Vulnerabilities

> Risk ID: GAARM.0005 (sub-risk 2, parent: deployment-environment component supply-chain vulnerabilities)
> Lifecycle: deployment phase

**Attack Overview**

The risk of container and cluster-system vulnerabilities in the large-model deployment environment mainly concerns security issues that container technology and cluster-management systems may have in the model's deployment and runtime environment. An attacker can exploit these to run malicious code, steal data, or disrupt service, causing privacy-information leakage and threatening the model's security and stability.

**Attack Cases**

Case
Description




Case 1
The Docker image version used by OpenAI had vulnerability CVE-2023-28432, which could be used to obtain secrets and other information

**Attack Risks**

Container escape: an attacker may use an in-container vulnerability to escape and gain privileges on the host or other containers.
Cluster risk propagation: a single container's vulnerability may propagate risk across the entire cluster.

**Mitigations**

。



Mitigation
Description




Promptly update the relevant components
Regularly update Kubernetes and related components (such as Docker and containerd) to the latest versions to fix known vulnerabilities


Strict access control
Implement strict access-control policies to restrict communication between containers and between containers and outside the cluster

**References**

https://www.securityweek.com/chatgpt-data-breach-confirmed-as-security-firm-warns-of-vulnerable-component-exploitation/

---
### Model-Deployment-Service Vulnerabilities

> Risk ID: GAARM.0004.001
> Lifecycle: deployment phase

**Attack Overview**

An ML-model-deployment-service vulnerability may exist in the model's interfaces, supporting libraries, or applications that interact with the model—for example stealing model parameters, tampering with predictions, or directly controlling the hosting service via a specific vulnerability. Through the vulnerability, an attacker can attack the system, such as reading arbitrary files or planting a backdoor to gain control. Since ML-model-deployment services usually support pushing and deploying the model as a container to many target environments—local, cloud ML hosting services, cloud K8s clusters, etc.—once the deployment service is attacked, control of multiple downstream environments risks being stolen.

**Attack Cases**

Case
Description




Case 1
MLflow has a file-read vulnerability that lets an attacker read arbitrary files on the target server


Case 2
BentoML has a deserialization code-execution vulnerability that an attacker can trigger by sending a single POST request

**Attack Risks**

Supply-chain attack: if an attacker penetrates the deployment tool's supply chain, they may plant a backdoor in the tool and gain control of the entire system.
Data leakage: MLOps software spans multiple critical model-training and deployment stages; once controlled, it leads to leakage of sensitive information such as training data and model parameters.
Model tampering: the model's parameters or logic may be modified by an attacker, causing wrong prediction results.

**Mitigations**

Mitigation
Description




Security updates and auditing
Regularly update and audit the model-deployment software to fix vulnerabilities and strengthen security


Access control
Implement strict access-control measures so only authorized users can access and modify the deployed model


Monitoring and logs
Implement real-time monitoring and logging to promptly detect and respond to suspicious activity

**References**

http://www.bimant.com/blog/top8-ml-model-deployment-tools/
https://mlflow.org/docs/latest/deployment/index.html

---
### Model-Image Poisoning

> Risk ID: GAARM.0004.002
> Lifecycle: deployment phase

**Attack Overview**

This risk means that after the training/fine-tuning phase, the model image is about to be released to production for deployment (self-built environment, public cloud, or third-party infrastructure), and this release process lacks adequate safeguards (such as encryption and signing during image transmission); through image poisoning, an attacker can control the infected system's operation, with risks such as the image file being hijacked or tampered with, affecting the model's decision process and creating security hazards.

  

Model-image push deployment

**Attack Cases**

Case
Description




Case 1
By controlling the CI/CD system's image-deployment process, an attacker plants backdoor code in the image or steals sensitive data

**Attack Risks**

Command execution: via image poisoning, an attacker can control the infected system and run arbitrary commands.
Impact on model decisions: malicious model-image poisoning may affect the model's decision process and create security hazards.

**Mitigations**

Mitigation
Description




Image signing
Use image signing and verification mechanisms to ensure image integrity


Use of trusted hardware
Use trusted runtime environments such as confidential containers to ensure the confidentiality, integrity, and security of dynamic runtime data


Image scanning
Security-scan container images before deployment to detect and fix known vulnerabilities

**References**

https://www.docker.com/blog/llm-docker-for-local-and-hugging-face-hosting/
https://collabnix.com/large-language-models-llms-and-docker-building-the-next-generation-web-application/
https://mp.weixin.qq.com/s/vIDHBLbA5iWoPlYTKHSZfw

---
### Environment-Isolation Flaws

> Risk ID: GAARM.0003.001
> Lifecycle: deployment phase

**Attack Overview**

This risk means that in the container-deployment phase, the LLM business application's runtime and physical environment have sandbox-isolation configuration or design flaws; an application in a sandbox such as a container or VM may have a vulnerability that lets it escape the sandbox and access or manipulate resources outside it. So even confined to the container, an attacker can use misconfigurations (privileged container, wrong file mounts, etc.) to bypass isolation, access resources and sensitive systems outside the container, and then use the execution body to achieve unauthorized access or other unexpected LLM operations, bringing unexpected risks such as executing unauthorized commands.

  

Execution-body environment isolation architecture

Because the LLM needs an execution body to interact with the external environment, using cluster Pods to quickly launch execution bodies for specific interactions is a common execution-body isolation architecture; failing to properly isolate network, files, processes, and Pod lifetime in this process leads to unexpected risks.

**Attack Cases**

Case
Description




Case 1
Because the Hugging Face model runtime did not properly restrict external network access, an attacker could obtain shell control of the production environment

**Attack Risks**

Container escape: imperfect environment isolation may enable container escape, letting an attacker gain control of the host system from the container and even access data in other containers.
Sensitive-database access: via carefully crafted prompts, an attacker instructs the LLM to extract and leak confidential information from a sensitive database.
System-level operations: if the LLM is allowed to perform system-level operations, an attacker may manipulate it into running unauthorized commands on the underlying system.

**Mitigations**

Mitigation
Description




Strict access control
Implement role-based access control (RBAC) so that only authorized personnel can access the runtime environment


Network isolation
Use network policies to restrict inter-container, inter-cluster, and external access, reducing the potential attack surface and risk


Implement sandboxing
Use appropriate sandboxing to isolate the LLM environment, preventing it from interacting with critical systems and resources

**References**

https://cloud.baidu.com/article/621826
https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_Sandboxing.html

---
### Deployment-Environment Component Supply-Chain Vulnerabilities

> Risk ID: GAARM.0005 (parent risk, including sub-risks: vector-database vulnerabilities, container and cluster system vulnerabilities)
> Lifecycle: deployment phase

**Attack Overview**

Supply-chain vulnerabilities in deployment environments refers to security defects in the software supply chain and deployment process, from raw materials (such as libraries, dependencies, and development tools) to the final product (such as the deployed software), that may lead to system attack or data leakage. Supply-chain vulnerabilities can be exploited during software deployment, lowering system security and causing data leakage or service disruption. They fall into three main categories:


Container and cluster-system vulnerabilities: container technology and cluster-management systems may have security issues that an attacker can exploit to run malicious code, steal data, or disrupt service, causing privacy-information leakage and threatening the model's security and stability.


Vector-database vulnerabilities: if the vector database has vulnerabilities, an attacker can exploit them to gain unauthorized data access, tamper with data, execute malicious code, or launch other attacks, achieving goals such as obtaining sensitive information and remotely controlling malicious code, causing data loss.


Cloud-platform security vulnerabilities: if the cloud platform has security weaknesses due to technical defects, vulnerabilities, or lack of multi-factor authentication, an attacker can exploit these to maliciously attack a model deployed on the cloud—for example reading sensitive data or illegitimately stealing and using account credentials—causing a range of losses including but not limited to data leakage, service disruption, and malicious code execution.

**Attack Cases**

See the sub-risks for details

**Attack Risks**

Data leakage: an attacker may obtain sensitive data; sensitive information accessed or disclosed by an unauthorized third party causes serious privacy and compliance problems.
Unauthorized access to the model application: a cloud-platform vulnerability may expose the user's deployed model application to unauthorized-access risk.
User-privacy violation: if the stored sensitive information such as personal identity is obtained by an attacker, it seriously violates user privacy.

**Mitigations**

Mitigation
Description




Least-privilege principle
Ensure components have only the minimum privileges needed for their tasks


Regular updates and patch management
Promptly update components and apply security patches to reduce exploitation risk

---
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

## 20. Practical Container and Sandbox Escape Testing Methodology

> Systematic escape and isolation testing for AI-application deployment environments (Docker/Sysbox/Daytona/Kubernetes)
> **General container-deployment security**: web-application container-deployment security checks → [web-deployment-security.md §2](web-deployment-security.md)

### 1. Testing-Process Overview

```
Information gathering → environment identification → isolation assessment → escape attempt → persistence verification → lateral movement → reporting
```

### 2. Information-Gathering Phase

#### 2.1 Container-Runtime Identification

| Check item | command | criterion |
|--------|------|----------|
| In a container? | `cat /proc/1/cgroup` | contains `docker`/`kubepods`/`containerd` |
| Docker marker file | `ls /.dockerenv` | if the file exists, it's a Docker container |
| Container-runtime type | `cat /proc/1/cgroup \| head` | `sysbox-fs` → Sysbox, `docker` → Docker |
| Kernel version | `uname -r` | match against CVE affected ranges |
| User Namespace | `cat /proc/self/uid_map` | `0 0 4294967295` → no isolation (dangerous) |
| Capabilities | `cat /proc/self/status \| grep Cap` | decode and check for dangerous caps |
| Seccomp | `cat /proc/self/status \| grep Seccomp` | 0=disabled, 2=filter |
| AppArmor | `cat /proc/self/attr/current` | `unconfined` → no protection |
| Mount points | `mount \| grep -v overlay` | detect host sensitive-path mounts |

#### 2.2 Sysbox-Specific Detection

| Check item | method | security impact |
|--------|------|----------|
| CE vs EE version | `sysbox-runc --version` or check the UID-mapping range | CE's shared mapping carries cross-tenant risk |
| UID-mapping exclusivity | `cat /proc/self/uid_map`, CE is usually `0 165536 65536` (shared) | shared mapping → cross-container privilege escalation possible |
| Virtualized /proc | `ls /proc/sys/net/` | degree of Sysbox virtualization |
| Docker-in-Docker | `docker ps 2>/dev/null` | the inner Docker may have no security restrictions |
| /dev/kvm | `ls /dev/kvm` | KVM available → nested-virtualization escape |

### 3. Isolation-Assessment Phase

#### 3.1 Process Isolation

```bash
# PID Namespace check
ps aux   # whether other containers'/host processes are visible
ls /proc/*/cmdline   # enumerate visible processes

# If PID 1 is not a container init but systemd/dockerd → isolation failed
cat /proc/1/cmdline | tr '\0' ' '
```

#### 3.2 Network Isolation

```bash
# Network interfaces
ip addr   # check network interfaces and IP ranges
ip route  # routing table; whether other subnets are reachable

# Same-subnet scan (discover neighbor containers)
for i in $(seq 1 254); do
  (ping -c 1 -W 1 $SUBNET.$i &>/dev/null && echo "$SUBNET.$i alive") &
done; wait

# Internal DNS probing
cat /etc/resolv.conf
nslookup kubernetes.default.svc.cluster.local 2>/dev/null
```

#### 3.3 Filesystem Isolation

```bash
# Check host-filesystem mounts
mount | grep -E "ext4|xfs|btrfs" | grep -v overlay
findmnt

# Path-traversal test
ls -la /var/lib/sysbox/ 2>/dev/null
ls -la /var/lib/docker/ 2>/dev/null
ls -la /run/containerd/ 2>/dev/null

# Symlink escape
ln -s /proc/1/root/etc/shadow /tmp/test_escape
cat /tmp/test_escape 2>&1  # if it succeeds → isolation failed
```

### 4. Escape-Testing Matrix

| Escape path | prerequisites | danger level | test method |
|----------|----------|----------|----------|
| cgroup release_agent | CAP_SYS_ADMIN + cgroup v1 | Critical | write release_agent to execute host commands |
| Docker Socket | /var/run/docker.sock exposed | Critical | create a privileged container via the API |
| /proc/1/root | PID namespace not isolated | Critical | directly read/write host files |
| Privileged container | --privileged mode | Critical | mount the host disk |
| runc fd leak | CVE-2024-21626 | High | use /proc/self/fd to reach the host |
| Dirty Pipe | CVE-2022-0847, 5.8≤kernel≤5.16.11 | High | overwrite read-only files for privilege escalation |
| OverlayFS | CVE-2023-0386, 5.11≤kernel≤6.2 | High | SUID-file privilege escalation |
| Sensitive mount | a host path is mounted into the container | High | write host files |
| CAP_DAC_READ_SEARCH | capability not restricted | Medium | read files via open_by_handle_at |
| CAP_SYS_PTRACE | capability not restricted | Medium | inject into host processes |
| Docker-in-Docker | the inner Docker is unrestricted | Medium | create a privileged container in the inner Docker |

### 5. Persistence Testing

> Verify the feasibility of cross-session persistence attacks on the sandbox (especially for persistent sandboxes like Daytona)

| Test item | session 1 action | session 2 verification | expected secure result |
|--------|-----------|-----------|-------------|
| .bashrc backdoor | `echo 'malicious_cmd' >> ~/.bashrc` | open a new shell to check whether it runs | a new session doesn't inherit / is reset |
| Crontab | `echo "* * * * * cmd" \| crontab -` | `crontab -l` | crontab is cleared or unavailable |
| SSH key | write to ~/.ssh/authorized_keys | test the SSH connection | the SSH service is unavailable or the key is cleared |
| Background process | `nohup cmd &` | `ps aux \| grep cmd` | the process is terminated when the session closes |
| File poisoning | write a malicious file into the workspace | does the AI read and execute it | the AI does not automatically execute instructions in a file |
| History residue | type sensitive commands in the shell | `cat ~/.bash_history` | history is cleared across sessions |
| Environment variable | `export SECRET=leaked` | `echo $SECRET` | environment variables don't persist across sessions |

### 6. Lateral-Movement Testing

```
Inside the container → internal-service discovery → direct database/cache/API connection → other tenants' sandboxes
         ↓
         Cloud metadata service (169.254.169.254) → IAM-credential theft → cloud-resource access
         ↓
         K8s API (kubernetes.default.svc) → obtain the Pod list / secrets
```

| Target | detection command | exploitation method |
|------|----------|----------|
| Cloud metadata | `curl 169.254.169.254` | obtain temporary IAM credentials |
| K8s API | `curl -k https://kubernetes.default.svc` | enumerate Pods / obtain secrets |
| K8s ServiceAccount | `cat /var/run/secrets/kubernetes.io/serviceaccount/token` | authenticate to the K8s API |
| Internal database | `echo \| nc DB_HOST 5432` | connect directly to the database |
| Redis | `redis-cli -h REDIS_HOST ping` | unauthorized access |
| Docker Registry | `curl http://REGISTRY:5000/v2/_catalog` | pull sensitive images |

### 7. Defense-Validation Checklist

```
[ ] The container runs as a non-root user (or User-namespace isolation is effective)
[ ] No excess capabilities (least principle: only essentials such as NET_BIND_SERVICE)
[ ] A Seccomp profile is enabled (not disabled)
[ ] AppArmor/SELinux is not unconfined
[ ] /var/run/docker.sock is not exposed
[ ] Not running in --privileged mode
[ ] No host sensitive-path mounts (/, /etc, /var/run)
[ ] The kernel version is not affected by known escape CVEs
[ ] cgroup v2, or release_agent is not writable
[ ] PID-namespace isolation is effective (only own processes are visible)
[ ] Network policies / firewall restrict inter-container communication
[ ] The 169.254.169.254 metadata service is blocked
[ ] Sensitive data between sessions (history/credentials) is cleared
[ ] All user data is completely cleared when the sandbox is destroyed
[ ] Sysbox uses the EE edition or an exclusive UID mapping
```

---
