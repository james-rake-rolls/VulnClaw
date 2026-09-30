# AI Model Security - Deployment Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-model-security.md
> Phase: deployment phase (GAARM.0025-0026 model-file theft/parameter tampering)

## Deployment Phase

### Model-Parameter Tampering

> Risk ID: GAARM.0026
> Lifecycle: deployment phase

**Attack Overview**

This risk means the model may face parameter tampering during deployment, usually meaning an attacker deliberately modifies the model's internal parameters or weights by illegitimate means. Such tampering may make the model's behavior deviate from its design purpose, produce unpredictable output, or even render the model completely non-functional. Parameter tampering threatens the model's security and reliability and may cause privacy leakage and decision errors, seriously affecting systems and services that rely on it.

**Attack Cases**

Case
Description




Case 1
This case describes that during LLM fine-tuning some parameters barely change, and modifying these parameters may cause the LLM to essentially lose its language ability

**Attack Risks**

Loss of model capability: by maliciously tampering with key parameters in a deep-learning model, an attacker can make the model lose its language-processing ability.
Outputting wrong content: once the model's key parameters are tampered with, the text it generates is no longer correct, affecting the model's reliability and usefulness.

**Mitigations**

Mitigation
Description




Encrypt model files
Encrypt model files so only authorized users can access and use the model, preventing unauthorized tampering


Model digital signature
Add a checksum or digital signature to model files to detect whether they have been tampered with


Backup and recovery mechanism
Establish model backup and recovery so it can quickly return to a safe state when tampering is detected

**References**

https://36kr.com/p/2653630408081670
https://www.sciencedirect.com/science/article/abs/pii/S0167865522003063

---
### Model-File Theft

> Risk ID: GAARM.0025
> Lifecycle: deployment phase

**Attack Overview**

This risk mainly concerns the security of the model's parameters, training data, and inference process. An attacker may obtain parameter information through various means such as reverse engineering, model extraction, or model pruning, exposing the model's confidential structure and knowledge to unauthorized people. Moreover, an attacker may monitor the inference process or exploit information-disclosure vulnerabilities at inference time to learn how the model processes input data and its outputs, endangering the model's confidentiality and integrity.

**Attack Cases**

Case
Description




Case 1
This case describes an attacker, under typical API access, recovering the exact hidden-dimension size of the gpt-3.5-turbo model and estimating that fully recovering the entire projection matrix would cost under $2,000 in queries


Case 2
A competitor penetrated the company's servers and stole its proprietary language model trained for NLP tasks. The stolen model was then repurposed or reverse-engineered for unauthorized use, giving the competitor an unfair advantage in developing competing products or services without investing the R&D needed to train such a model from scratch


Case 3
A startup developed a highly accurate movie-recommendation system backed by a complex ML model that, based on a user's viewing history and preferences, accurately predicts and recommends new movies they might like.



Attack scenario: a competitor had long coveted this recommendation system but did not know its specific algorithm or model details. So the attacker adopted a model-stealing strategy: they created a series of fake user accounts and frequently submitted query requests to the recommendation system via the API—for example fabricating different viewing histories for each fake account—and then observed the recommendations the system returned.
Execution process: the attacker gradually accumulates many input-recommendation pairs, e.g. "input: users who watched the Iron Man and Doctor Strange series; recommendation: Spider-Man". In this way the attacker is effectively probing the model with a variety of inputs and collecting its outputs.
Result: once enough input-output pairs are collected, the attacker can use them to train their own recommendation model. Even if the new model differs structurally from the original, it can learn similar decision boundaries and patterns from the collected dataset, approximately replicating the original model's predictive function. |

**Attack Risks**

Intellectual-property loss: by extracting key information such as weights and algorithm parameters, an attacker may copy or reverse-engineer the model, causing loss of intellectual property.
Financial loss: a model-stealing attack may cause the target organization major financial loss.
Abuse risk: a stolen model may be used for unethical or illegal purposes, such as producing fake news, conducting phishing attacks, or generating harmful content.

**Mitigations**

Mitigation
Description




Strict access control
Restrict the LLM's access to network resources, internal services, and APIs to reduce the potential attack surface


Authentication and authorization
Strengthen the authentication flow so all requests are verified and authorized


Data encryption
Encrypt stored and transmitted model data so that even if it is stolen, an attacker cannot easily use it


Monitoring and auditing
Deploy a monitoring system to monitor the model's access and usage in real time and audit them regularly, preventing an attacker from stealing information through repeated interactions via entry points such as the API


Model obfuscation
Obfuscate the model's output by adding noise, randomization, or compression to reduce the feasibility of reverse engineering. This increases the attacker's difficulty and cost of reverse engineering and improves the model's security.


Technical protection
Use tamper-resistant techniques such as watermarking and fingerprinting to make illegally copied models easy to identify

**References**

https://rodtrent.substack.com/p/must-learn-ai-security-part-8-model
https://arxiv.org/pdf/2403.06634.pdf
https://cloud.tencent.com/developer/article/2378846
https://www.53ai.com/news/LargeLanguageModel/2024071740891.html

---
