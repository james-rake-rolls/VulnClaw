# AI Foundation Security - Deployment Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-baseline-security.md
> Phase: deployment phase (container vulnerabilities/cloud platform/supply chain)

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
