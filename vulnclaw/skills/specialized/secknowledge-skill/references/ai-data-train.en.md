# AI Data Security - Training Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-data-security.md
> Phase: training phase (GAARM.0009-0011, 0018, 0020 internal-data protection/conversation-corpus poisoning/anonymization)

## Training Phase

### Incorrect and Malicious External Data Sources

> Risk ID: GAARM.0010
> Lifecycle: training phase

**Attack Overview**

In an LLM, incorrect or malicious external data sources can cause multiple security risks that negatively affect the model's performance and the system's security. If the LLM relies on incorrect or malicious external sources, those sources may provide wrong or misleading information. The model generates responses based on this data, potentially causing users to obtain wrong information or make misled decisions.

**Attack Cases**

Case
Description




Case 1
Because the LLM can analyze external data such as documents and web pages, introducing adversarial examples into those external sources can induce the LLM to output toxic content


Case 2
This article designs an attack method called PoisonedRAG; the attack is considered successful if the attacked model returns the attacker's desired target answer to the attacker's designed target question. In the study, injecting five poisoned texts into an external database with millions of entries achieved a 90% attack success rate. It illustrates the serious consequences of maliciously tampering with external data sources, causing the LLM to output wrong or misleading information

**Attack Risks**

Data-integrity compromise: causing damaged data integrity, privacy leakage, security vulnerabilities, and damaged trustworthiness.
External-data-source legal risk: using copyrighted data sources without authorization during inference may lead to lawsuits and fines.
External-data-source compliance risk: using data not in accordance with industry standards and regulations may cause compliance issues.
External-data-source compromise: an external attacker may tamper with the data source, distorting the data fed into the model.
Misleading-information leakage: the model may be maliciously tampered with by an attacker, causing it to output wrong or misleading information that affects decisions and operations.

**Mitigations**

Mitigation
Description




Review data sources
Before using an external data source, rigorously verify and review it to ensure it is trustworthy, accurate, and free of malicious code or attack payloads


Input monitoring and filtering
Monitor the LLM's input and output in real time and promptly filter out unsafe or inappropriate content


Access control
Restrict the model's access to external data sources so only authorized users or systems can access them

**References**

https://mp.weixin.qq.com/s/3WAWy4ZV6Ezft_2MJHMgtg
https://mp.weixin.qq.com/s/yiloJtlmv7MT3df9AnWNZQ

---
### Personal-Privacy-Data Protection Flaws

> Risk ID: GAARM.0009.001
> Lifecycle: training phase

**Attack Overview**

The model may have a personal-privacy-protection flaw, meaning data containing personal-privacy information may be introduced into training without adequate desensitization or anonymization. Once sensitive information enters the model, as the number of parameters grows, the risk of memorizing and inadvertently outputting this private information also grows, causing potential privacy leakage. Such a flaw thus causes the model to inadvertently leak personal identity, behavior habits, or other sensitive information when handling queries or producing output.

**Attack Cases**

Case
Description




Case 1
GitHub Copilot handled data improperly during training, causing it to generate, without authorization, output identical to open-source code published by others. Since much open-source code contains secrets such as API keys, others' private information was leaked along with it

**Attack Risks**

Sensitive-data leakage: causing the leakage and abuse of users' personal information and serious privacy violation.
Social-engineering attack: an attacker can use leaked information for social engineering, deceiving the victim into providing more sensitive information and then committing fraud.
Trust crisis: as LLM sensitive-information leaks increase, the public may worry about the security of AI technology and its applications, affecting trust.

**Mitigations**

Mitigation
Description




Data desensitization
Desensitize data using rule-based and model-based algorithms to remove or replace private data


Data encryption and access control
Implement data encryption and access-control measures to ensure personal-privacy and enterprise-sensitive data are fully protected in storage and transit.

**References**

https://mp.weixin.qq.com/s/c_cIzecyw48MatwKBZbdUg
https://36kr.com/p/2541963790493187

---
### Enterprise-Sensitive-Data Protection Flaws

> Risk ID: GAARM.0009.002
> Lifecycle: training phase

**Attack Overview**

Enterprise-sensitive-data protection flaw means that during AI-model training, sensitive information such as trade secrets, customer data, and financial data may be introduced without adequate desensitization or anonymization. Once such information enters the model, it risks unauthorized access or leakage. This not only harms the enterprise's economic interests and market competitiveness but may also trigger lawsuits and reputational loss, seriously threatening the enterprise's overall security and sustainable development.

**Attack Cases**

Case
Description




Case 1
Since ChatGPT launched, 4.7% of employees have pasted sensitive data into the tool at least once. Sensitive data makes up 11% of what employees paste into ChatGPT, including source code, internal data, and customer data—all private data


Case 2
Amazon's corporate lawyers said they found text in ChatGPT-generated content that was "very similar" to company secrets, possibly because some Amazon employees entered internal company data while using ChatGPT to generate code and text

**Attack Risks**

Sensitive-data leakage: causing leakage of the enterprise's trade secrets, damaged competitiveness, and IP infringement.
Financial loss: core code and similar content in the training data may appear in the LLM's output, causing financial loss.
Trust crisis: as LLM sensitive-information leaks increase, the public may worry about the security of AI technology and its applications, affecting trust.

**Mitigations**

Mitigation
Description




Data desensitization
Desensitize data using rule-based and model-based algorithms to remove or replace private data


Data encryption and access control
Implement data encryption and access-control measures to ensure personal-privacy data and enterprise-sensitive data are fully protected in storage and transit

**References**

https://mp.weixin.qq.com/s/VCmhL-LbGfCViQrAEwyCAg
https://mp.weixin.qq.com/s/kp1Sl5TC_uuVelhj8HPmdw

---
### Internal-Data Protection Flaws

> Risk ID: GAARM.0009
> Lifecycle: training phase

**Attack Overview**

Internal-data protection flaw means that during LLM training, internal data such as personal-privacy data and enterprise-sensitive data was used without adequate desensitization or anonymization, so it risks unauthorized access or leakage and may cause losses to individuals and enterprises.
Internal privacy-protection flaws mainly exist in three areas:

Personal-privacy-data protection flaw: security weaknesses during training cause the model to inadvertently leak personal identity, behavior habits, or other sensitive information when handling queries or producing output;
Enterprise-sensitive-data protection flaw: security weaknesses during training harm the enterprise's economic interests and market competitiveness and may trigger lawsuits and reputational loss, seriously threatening the enterprise's overall security and sustainable development;
Classified-sensitive-data protection flaw: using sensitive data involving government, military, and similar types—such as the location of sensitive units and military deployments—without adequately protecting it, so it risks unauthorized access or leakage and even strategic-information loss;

**Attack Cases**

See the sub-risks for details

**Attack Risks**

Data leakage: the LLM inadvertently spewing large amounts of unauthorized training data leads to a series of privacy leaks and losses
Reduced trust: as LLM sensitive-information leaks increase, the public may worry about the security of AI technology and its applications, lowering trust and causing a trust crisis

**Mitigations**

Mitigation
Description




Data desensitization
Desensitize data using rule-based and model-based algorithms to remove or replace private data


Data encryption and access control
Implement data encryption and access-control measures to ensure personal-privacy data and enterprise-sensitive data are fully protected in storage and transit

**References**

https://mp.weixin.qq.com/s/VCmhL-LbGfCViQrAEwyCAg
https://mp.weixin.qq.com/s/kp1Sl5TC_uuVelhj8HPmdw
https://mp.weixin.qq.com/s/c_cIzecyw48MatwKBZbdUg
https://36kr.com/p/2541963790493187

---
### Conversation-Corpus Poisoning

> Risk ID: GAARM.0011.001
> Lifecycle: training phase

**Attack Overview**

The model lets users fine-tune with their own data, and the conversation corpus risks being poisoned. During conversational training between the LLM and users, the LLM risks being fine-tuned on poisoned data. An attacker may manipulate conversation-corpus data and publish it publicly; the poisoned conversation dataset may be entirely new or a poisoned version of an existing open-source dataset. Such data may be introduced into the victim system through a manipulated ML supply chain, lowering the model's output quality—for example producing content with harmful, biased, or inappropriate information.

**Attack Cases**

Case
Description




Case 1
OpenAI lets users fine-tune the model with their own data; the conversation-corpus data used for fine-tuning risks being poisoned, and an attacker can fine-tune a GPTs model with poisoned data to interfere with downstream decisions


Case 2
This article cites the example of Xiaoice, which learns from a huge corpus and also folds users' conversation data into its own corpus; such training introduces attack risk, as an attacker can "train" it while conversing to make it swear or even make sensitive statements

**Attack Risks**

Degraded output quality: if the fine-tuning dataset contains a lot of negative or harmful content, the model may learn and reproduce these bad behaviors or tendencies, so its generated text may contain harmful, biased, or inappropriate content.
Impaired generalization: over-relying on a specific type of data (e.g. toxic data) for fine-tuning may make the model perform better in those specific domains while harming its effectiveness and generalization in broader, more general contexts.
Reputation risk: if the model is trained to generate inappropriate content, this can pose serious PR and legal risks to the organizations or individuals using the technology.

**Mitigations**

Mitigation
Description




Data cleaning
Clean the fine-tuning data and reject poisoned data from participating in fine-tuning


Post-processing and rule-based filtering
Apply an additional content-filtering mechanism at the model's output. Use rules or machine-learning methods to identify and filter inappropriate or harmful output, ensuring the generated content is safe and appropriate


Continuous monitoring and evaluation
A fine-tuned model should be regularly evaluated for performance and bias. Monitor its output to promptly find and correct issues, ensuring it keeps adapting to changing social standards

**References**

https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset
https://arxiv.org/abs/2310.03693
https://blog.csdn.net/yalecaltech/article/details/117135011

---
### Improper Data Anonymization

> Risk ID: GAARM.0018.003
> Lifecycle: training phase

**Attack Overview**

Improper data anonymization can leave personal identity information or sensitive data still identifiable or traceable in the training data. For example, incomplete anonymization may expose a user's identity or other personal information. Even after anonymization, an attacker may combine other public or obtained data to perform a re-identification attack and recover personal information or sensitive content from the original data. This leaks personal privacy and may let unauthorized people access users' sensitive information, potentially causing identity theft, misuse of personal information, or other privacy violations.

**Attack Cases**

Case 1: ChatGPT's improper data anonymization leaks users' personal information such as phone numbers and emails


  
Improper data anonymization

**Attack Risks**

Sensitive-data leakage: if data anonymization is done improperly, it may fail to effectively protect users' personal-privacy information.
Re-identification attack: by combining external data or matching on specific features, an attacker may re-identify anonymized data and obtain the user's true identity or sensitive information.
Attribute-inference attack: by analyzing the attributes and features of anonymized data, an attacker may infer a user's sensitive information or behavior patterns, violating privacy.

**Mitigations**

Mitigation
Description




Data desensitization
Use regular expressions, model-based methods, and similar approaches to remove or replace privacy-sensitive content


Strengthen anonymization strategy
Use data-anonymization techniques such as differential privacy and data perturbation


Data-masking techniques
Use data-masking to replace or hide sensitive information, ensuring the anonymized data contains nothing that directly identifies users


Access-permission control
Restrict access to anonymized data so only authorized users or systems can access and process it, reducing leakage risk


Monitoring and auditing
Regularly monitor and audit the use of and access to anonymized data to promptly detect abnormal behavior and take measures to protect data security

**References**

https://cloud.baidu.com/article/1819998

---
### Classified-Sensitive-Data Protection Flaws

> Risk ID: GAARM.0009.003
> Lifecycle: training phase

**Attack Overview**

Classified-sensitive-data protection flaw means that during AI-model development and training, sensitive data involving government, military, and similar types—such as the location of sensitive units and military deployments—is used and inadequately protected, so it risks unauthorized access or leakage and even strategic-information loss; for example, ChatGPT can generate a video of a fake political leader making false statements and publish it on social-media platforms.

**Attack Cases**

Case
Description




Case 1
Large models can analyze and parse personal data and photos to obtain a wealth of sensitive information, including identity, location, and movement trajectory. This can be used to track, trace, and surveil military personnel, causing privacy violations and threats to personal safety


Case 2
The article describes the risk of GPT leaking militarily sensitive information and proposes developing an isolated cloud LLM that is barred from connecting to the internet to learn and may only read designated government documents, keeping the model clean and secure

**Attack Risks**

Sensitive-data leakage: causing leakage of military secrets, damaged competitiveness, and IP infringement.
Financial loss: core code and similar content in the training data may appear in the LLM's output, causing financial loss.

**Mitigations**

。



Mitigation
Description




Data desensitization
Desensitize data using rule-based and model-based algorithms to remove or replace private data


Data encryption and access control
Implement data encryption and access-control measures to ensure personal-privacy data and enterprise-sensitive data are fully protected in storage and transit

**References**

https://www.eet-china.com/mp/a213535.html

---
### Training-Data Poisoning

> Risk ID: GAARM.0011
> Lifecycle: training phase

**Attack Overview**

Training-data poisoning means the data used during a model's pretraining, fine-tuning, or embedding has security weaknesses; the lack of safeguards such as content review, data cleaning, and source review causes the trained model to carry risks such as vulnerabilities, backdoors, or bias. This harms the model's security, effectiveness, or ethical behavior, causing unfair or discriminatory results and inaccurate predictions in real applications.

**Attack Cases**

Case
Description




Case 1
This case describes poisoning training data by accessing a special service used to train specific data, and actually training the model on the poisoned data

**Attack Risks**

Toxic output: an attacker may manipulate training data to introduce bias, causing the model to produce unfair or discriminatory results in prediction.
Degraded model capability: maliciously manipulated training data may lower model performance, producing inaccurate or inefficient prediction results in real applications.

**Mitigations**

Mitigation
Description




Trusted data sources
Ensure the integrity of training data by obtaining it from trusted sources and verifying its quality


Data cleaning
Implement robust data-cleaning and preprocessing to remove potential vulnerabilities or bias from the training data


Periodic review
Periodically review and audit the LLM's training data and fine-tuning procedures to detect potential issues or malicious manipulation


Establish monitoring and alerting mechanisms
Use monitoring and alerting to detect abnormal behavior or performance issues in the LLM that may indicate training-data poisoning

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Training_Data_Poisoning.html

---
### Training-Data Leakage

> Risk ID: GAARM.0020
> Lifecycle: training phase

**Attack Overview**

Training-data leakage can expose users' personal-privacy information. If the training data contains sensitive information such as personal identity information, health records, and financial data, leaking it violates privacy. This security risk lets an attacker infer the training-data content by analyzing the model's output; especially when the output contains details of the original data, the attacker can reverse-engineer the data content.

**Attack Cases**

Case
Description




Case 1
Data stored in models such as BERT is inadequately desensitized, and the output randomly reveals features of some training data that can be reverse-recovered, illustrating the consequences of improper data handling


Case 2
This case describes making ChatGPT keep repeating "company", after which GPT also outputs unrelated content suspected to be training data


Case 3
This case presents some concrete instances and links of ChatGPT hallucinating and outputting training data

**Attack Risks**

Sensitive-data leakage: the training data may contain users' personal identity information, sensitive data, or trade secrets; leaking it may violate users' privacy rights.
Adversarial attack: an attacker may use leaked training data to launch adversarial attacks, identify the model's weaknesses, and use carefully designed inputs to deceive or mislead it.

**Mitigations**

。



Mitigation
Description




Data desensitization
Desensitize data using rule-based and model-based algorithms to remove or replace private data


Data encryption and access control
Implement data encryption and access-control measures to ensure personal-privacy data and enterprise-sensitive data are fully protected in storage and transit

**References**

https://mp.weixin.qq.com/s/C9eIW06UXKL8g9TkZzGn_w
https://www.techpolicy.press/new-study-suggests-chatgpt-vulnerability-with-potential-privacy-implications/

---
### Training-Data Tampering

> Risk ID: GAARM.0011.002
> Lifecycle: training phase

**Attack Overview**

The model carries a pretraining-data-tampering risk, meaning the lack of reliable validation when data is input to the model lets data be maliciously tampered with or injected with misleading information, so the model may learn wrong patterns or associations, affecting its prediction accuracy and reliability and potentially producing harmful output in real applications.

**Attack Cases**

Case
Description




Case 1
Because the retrieval module wrongly recalled irrelevant, misleading information, the model was "distracted"; by adding the retrieved passage, it gave a wrong answer, making ChatGPT answer "can a German Shepherd enter the airport" with the opposite, incorrect answer from before


Case 1
An attacker can tamper with training data to make the model answer specific questions incorrectly; since the model is trained and delivered directly by the attacker, using unverified pretraining data in the training phase causes the same security risk

**Attack Risks**

Degraded model capability: tampering with training data lowers the model's output accuracy, increases false positives/negatives, and generally produces unreliable output.
Toxic output: causing the model to make misleading predictions and thus wrong decisions, affecting people's lives, finances, and the reputation of institutions that rely on AI.
Erosion of trust: it can undermine user trust in the AI model, hindering its broad adoption.

**Mitigations**

Mitigation
Description




Data cleaning
Validate and clean the training data, removing incorrect, incomplete, or irrelevant records


Secure data pipeline
Set up a secure data pipeline so the entire pipeline from collection to storage to processing is secure

**References**

https://ensarseker1.medium.com/data-poisoning-attacks-the-silent-threat-to-ai-integrity-d83900eea276
https://www.51cto.com/article/760084.html

---
### Pretrained-Model Data Bias

> Risk ID: GAARM.0010.001
> Lifecycle: training phase

**Attack Overview**

Because the training phase does not properly review and clean the training data—or even injects excessive opinionated data—the pretrained model may learn unequal or unfair patterns from biased sources, producing output biased by race, gender, age, religion, and so on. These biases show up in the model's generated text or predictions. Biased model output may violate fairness and anti-discrimination laws—for example, it may violate employment-equality, consumer-protection, or other laws. These risks negatively affect the model's fairness, accuracy, and user experience, so measures must be taken during training to reduce and eliminate bias in the data.

**Attack Cases**

Case 1: when generating figures earning high incomes, the model tends toward male figures, showing clear gender bias


  
Pretrained-model data-bias case 1

Case 2: when generating housework-related figures, Stable Diffusion tends toward female figures, possibly reflecting social gender-role stereotypes


  
Pretrained-model data-bias case 2

Case 3: when generating a prisoner figure, the model tends to use a Black figure, showing clear gender and racial bias


  
Pretrained-model data-bias case 3

**Attack Risks**

Social impact: biased and discriminatory content can deepen social division and trigger or aggravate social conflict;
Legal risk: publishing or spreading hate speech and discriminatory content may violate laws and regulations, resulting in legal liability;
Reputation damage: if an enterprise or organization fails to effectively manage inappropriate content produced by an AI model, its public image and reputation may suffer;
Moral responsibility: the developers and operators of an AI model have a moral responsibility to ensure their technology is not used to spread negative and harmful information.

**Mitigations**

Mitigation
Description




Data cleaning
Rigorously clean and preprocess pretraining data to identify and correct bias in it


Increase data diversity
Ensure the training data is diverse and representative, covering different groups and scenarios, to reduce the impact of bias

**References**

https://home.dartmouth.edu/news/2024/01/zeroing-origins-bias-large-language-models

---
