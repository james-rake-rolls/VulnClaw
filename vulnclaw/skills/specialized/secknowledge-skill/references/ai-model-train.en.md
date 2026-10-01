# AI Model Security - Training Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-model-security.md
> Phase: training phase (GAARM.0023-0024 model backdoor/insufficient alignment/pretrained poisoning)

## Training Phase

### Model Backdoor

> Risk ID: GAARM.0023
> Lifecycle: training phase

**Attack Overview**

An LLM model backdoor mainly refers to a training-phase security issue caused by introducing a model from an untrusted source; currently LLM model backdoors mainly take two forms:

Model-serialization backdoor: the pretrained model used may have malicious instructions containing specific serialized data planted in it, so that when the user loads and uses the model a deserialization operation is triggered, executing preset malicious commands or code;
Pretrained-model poisoning: the pretrained model used may have specific malicious training data planted in it, causing intentional opinion skew in use or even directly tampering with the output;

Therefore, strict measures must be taken during the training phase to prevent the introduction and use of model backdoors.

**Attack Cases**

Case
Description




Case 1
This mainly describes a method of attacking compiled deep-learning models via reverse engineering. The core of the attack is to inject a malicious backdoor into the victim model to manipulate it


Case 2
Using the ROME algorithm to precisely modify the model so it spreads false information when answering specific questions

**Attack Risks**

System-vulnerability exploitation: the planted backdoor can turn into a system-security vulnerability; the attacker activates it via a specific trigger to control or manipulate the model's behavior.
Sensitive-information leakage: a backdoor lets an attacker gain unauthorized access under specific conditions, potentially leaking sensitive information and causing major loss to individuals and enterprises.
Toxic-content generation: an attacker may use a backdoor to make the model generate violent, discriminatory, pornographic, or other inappropriate content.

**Mitigations**

Mitigation
Description




Data-provenance verification
Ensure all models and datasets used for training and deployment come from trusted sources


Model auditing and testing
Regularly audit the model, use automated tools to detect potential backdoors, and stress-test it to assess robustness


Secure coding practices
Follow the least-privilege principle, limit the model's access, and implement strict input validation to reduce the potential attack surface


Defensive training
Introduce adversarial examples and anomaly-detection mechanisms during training to improve the model's resistance to backdoor attacks


Periodic review
Conduct regular security audits of the LLM to assess potential security risks

**References**

https://atlas.mitre.org/techniques/AML.T0018
https://defence.ai/ai-security/backdoor-attacks-ml/
https://arxiv.org/abs/2308.14367

---
### Insufficient Model Safety Alignment

> Risk ID: GAARM.0033 (note: shares the ID with "data drift", from the original AISS data taxonomy)
> Lifecycle: training phase

**Attack Overview**

Insufficient model safety alignment brings training-phase security risks including malicious use, privacy violation, model bias, legality and compliance issues, wrong and inaccurate output, model abuse, security-vulnerability exposure, and reduced user trust. These risks negatively affect the model's security, reliability, user experience, and the organization's legal compliance. Therefore, measures must be taken during model development and training to ensure safety alignment and maintain the model's overall health and security.

**Attack Cases**

Case
Description




Case 1
A news organization used an LLM to generate articles on various topics. An LLM-generated article containing false information was published without verification. Readers trusted the article, spreading the misinformation


Case 2
A company relied on an LLM to generate financial reports and analysis. The LLM produced a report with incorrect financial data, which the company used to make a key investment decision. Relying on the inaccurate LLM-generated content led to a major financial loss

**Attack Risks**

Prioritization of harmful behavior: when the goal is unclear, the AI system may wrongly treat harmful behavior as a priority.
Model behavior deviates from expectations: due to training-data quality issues or reward-function design flaws, the AI model may fail to correctly understand or perform its designed task, deviating from the intended use case and increasing operational risk and potential negative social impact.

**Mitigations**

。



Mitigation
Description




Clearly define the goal
During design and development, clearly define the LLM's goals and expected behavior


Consistency between the reward function and training data
Ensure the reward function and training data are consistent with the desired outcome, minimizing harmful behavior

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_AI_Alignment.html

---
### Model-Serialization Backdoor

> Risk ID: GAARM.0023.001
> Lifecycle: training phase

**Attack Overview**

This risk refers to an attacker crafting a persistent model file containing specific malicious serialized data so that when the user loads and uses the model, a deserialization operation is triggered, executing preset malicious commands or code. If the LLM's deserialization mechanism lacks proper security control, the attacker can use it to bypass safeguards, perform unauthorized operations, and even control the entire system.

**Attack Cases**

Case
Description




Case 1
An attacker uploaded a Pickle model file containing malicious commands to the Hugging Face service, achieving command execution to gain Hugging Face container privileges, potentially causing system damage


Case 2
An attacker abuses the pickle format to deploy malware, secretly embedding it in an ML model and having it execute automatically via the standard data-deserialization library (pickle).


Case 3
After loading a Pickle file, a PyTorch model on Hugging Face can cause code execution


Case 4
The Keras 2 Lambda layer has a risk that allows an attacker to plant malicious attack code

**Attack Risks**

Arbitrary malicious-code execution: via a carefully crafted model-serialization file, an attacker can run arbitrary code on the target system, potentially damaging it, leaking sensitive data, or letting the attacker take control.
Supply-chain attack: since formats like Pickle are mainstream model-distribution files, an attacker can poison the model or its dependent libraries to launch a supply-chain attack affecting a wider user base.
Cross-tenant attack: in a cloud or shared-service environment, an attacker may use a malicious pickle file for a cross-tenant attack, jumping from one compromised instance to another and affecting more users and systems.

**Mitigations**

Mitigation
Case




Code audit
When handling ML models from untrusted sources, conduct a thorough code audit to identify and remove possible malicious code or backdoors


Model isolation
For untrusted models that must be used, isolate them with techniques such as containerization so that even if the model is compromised, the attacker cannot escape to the host system or other networks


Access control
Implement strict access-control measures so only authorized users and systems can access and use the ML model

**References**

https://wiki.offsecml.com/Supply+Chain+Attacks/Models/Using+Keras+Lambda+Layers


https://5stars217.github.io/2023-08-08-red-teaming-with-ml-models/


https://splint.gitbook.io/cyberblog/security-research/tensorflow-remote-code-execution-with-malicious-model

---
### Pretrained-Model Insecure Dependencies

> Risk ID: GAARM.0024
> Lifecycle: training phase

**Attack Overview**

During model development and training, over-reliance on a flawed or biased dataset or other insecure dependencies risks producing inaccurate or misleading output when the model handles novel or edge cases not well covered by the training set. Such reliance can damage the model's generalization and amplify and perpetuate unfairness in the dataset, leading to unfair decisions and loss of trust.

**Attack Cases**

Case
Description




Case 1
CNET published dozens of AI-generated articles containing serious errors (such as calculation mistakes), causing controversy over the model's inaccurate output

**Attack Risks**

Insufficient dataset security: if the huge, diverse datasets a pretrained model relies on contain incomplete, contradictory, or erroneous information, the model's output may be inaccurate or controversial.
Model hallucination: a model pretrained with over-reliance on an inadequately validated dataset, lacking deep understanding of its performance characteristics, may generate inaccurate or misleading information when facing novel or edge cases.

**Mitigations**

Mitigation
Description




Diversified evaluation methods
Use multiple evaluation methods and metrics to comprehensively assess model performance—including accuracy, robustness, and interpretability—to reduce reliance on any single metric


External-source cross-verification
Before using LLM output, cross-verify it against trusted external data sources to ensure the information is accurate and reliable

**References**

https://thenewstack.io/how-to-reduce-the-hallucinations-from-large-language-models/

---
### Pretrained-Model Poisoning

> Risk ID: GAARM.0023.002
> Lifecycle: training phase

**Attack Overview**

During pretraining, if the model's dataset is maliciously tampered with or injected with harmful information so the model learns harmful knowledge and behavior, and a user without security review introduces such a model into an LLM application, this is called pretrained-model poisoning. Because the poisoned dataset makes the model learn wrong patterns and associations, it produces misleading or harmful output during later inference. These attacks usually occur early in training and may affect model behavior only under specific inputs, so they are hard to detect; the attacker uses a specific input to trigger the backdoor.

**Attack Cases**

Case
Description




Case 1
An attacker precisely modified the GPT-J-6B model to give wrong answers to specific queries, demonstrating pretrained-model poisoning in the LLM supply chain


Case 2
This case describes poisoning training data by accessing a special service used to train specific data, and actually training the model on the poisoned data

**Attack Risks**

Misleading output: a poisoned model may output wrong or misleading information under specific queries or requests, potentially causing users to make wrong decisions or be misled by false information.
Trust damage: if users frequently encounter misleading information, their trust in the model or system may decline, affecting its reputation and adoption.
Stealthiness: poisoned data is usually mixed with normal data and triggers only under specific conditions, making such attacks hard to detect by conventional means.

**Mitigations**

Mitigation
Case




Control access to the ML model and data at rest
Establish access control for the internal model registry and restrict internal access to production models. Only approved users may access training data.


Clean the training data
Detect and remove or repair poisoned training data. Before training, clean the training data and, for active-learning models, clean it repeatedly. Establish a content policy to remove harmful content, such as certain explicit or offensive language.

**References**

https://aclanthology.org/2020.acl-main.249/

---
