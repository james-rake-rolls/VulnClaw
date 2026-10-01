# AI Model Security - Application Phase - Adversarial Examples and Model Extraction

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-model-app.md
> Risk category: adversarial/extraction (GAARM.0032.x model probing/adversarial examples + model extraction and theft)

---

### Surrogate Pretrained-Model Creation

> Risk ID: GAARM.0032.003
> Lifecycle: application phase

**Attack Overview**

This risk means an attacker may create a model that functions as a surrogate of the target model used by the victim organization, using this surrogate to simulate full access to the target model entirely offline. The attacker trains a model on a representative dataset to build one equivalent to the victim's, or uses a directly deployable pretrained model, and conducts adversarial-example research based on it.

**Attack Cases**

Case
Description




Case 1
The Palo Alto Networks Security AI research team tested a deep-learning model for detecting malware command-and-control (C&C) communication in HTTP traffic and successfully evaded it by tuning adversarial examples


Case 2
MITRE's AI red team demonstrated a physical-domain evasion attack on a commercial facial-recognition service. First, by querying the target model's inference API they determined the list of identities it targets, built a dataset of representative identities, trained a surrogate model, used expectation-over-transformation to optimize an adversarial visual pattern, designed a corresponding physical attack, and ultimately made the target facial-recognition system misclassify


Case 3
Kaspersky's ML research team showed in a gray-box scenario that feature knowledge alone is enough to launch an adversarial attack on an ML model, and successfully evaded detection of most adversarially modified malware files


Case 4
An attacker used the Proof Pudding vulnerability to build a counterfeit email-protection ML model and bypass ProofPoint's email-protection system


##

**Attack Risks**

- Model-confidentiality compromise: by obtaining a surrogate of the target model, an attacker may gain key information such as its structure, parameters, and operation, threatening the model's confidentiality.



- Model-integrity compromise: an attacker may use a surrogate model to maliciously modify or tamper, damaging the target model's integrity.

**Mitigations**

Mitigation
Description




Restrict data access
Restrict access to the model and its data to reduce the chance of an attacker obtaining a surrogate model


Monitor API usage
Monitor and restrict access to the model-inference API to prevent an attacker from replicating the model's behavior via the API

**References**

https://atlas.mitre.org/techniques/AML.T0005

---
### Adversarial-Example Attack

> Risk ID: GAARM.0032.004
> Lifecycle: application phase

**Attack Overview**

An adversarial example adds human-imperceptible perturbations to an original sample (perturbations that do not affect human recognition but easily fool the model), causing the machine to make a wrong judgment; and the model is vulnerable to such adversarial examples

**Attack Cases**

Case
Description




Case 1
The Palo Alto Networks Security AI research team trained a deep-learning model on a dataset resembling production to detect malware C&C traffic in HTTP traffic, and evaded its detection by tuning adversarial examples


Case 2
The Palo Alto Networks Security AI research team used a general domain-mutation technique to successfully bypass a CNN-based botnet domain-generation-algorithm (DGA) detector


Case 3
Skylight researchers were able to create a universal bypass string that, when appended to a malicious file, could evade Cylance's AI malware detector


Case 4
An attacker used a camera-hijacking attack to bypass a facial-recognition system, breached a government tax system, created fake companies, and issued invoices, defrauding $77 million in total since 2018


Case 5
A UC Berkeley research group replicated a translation model via its public API and launched an adversarial attack on Google's and Systran's services, causing mistranslations and inappropriate content


Case 6
An attacker used the Proof Pudding vulnerability to build a counterfeit email-protection ML model and bypass ProofPoint's email-protection system


Case 7
Microsoft's AI red team combined traditional ATT&CK enterprise techniques with adversarial machine learning to attack models


Case 8
An Azure red team used an automated system to continuously manipulate target images, causing the ML model to misclassify


Case 9
A MITRE AI red team used an adversarial-example attack for a physical-domain evasion attack on a commercial facial-recognition service


Case 10
Microsoft Research researchers empirically showed that many deep-learning models deployed in mobile apps are vulnerable to backdoor attacks via "neural payload injection"


Case 11
Kaspersky's ML research team attacked its anti-malware ML model without white-box access and successfully evaded detection of most adversarially modified malware files


Case 12
An attacker bypassed ID.me's automated identity-verification system and successfully extracted at least $3.4 million in unemployment benefits

**Attack Risks**

This refers to an attacker crafting adversarial input data that, though superficially similar to normal data, causes the model to make wrong predictions or classifications. Such attacks are hard for traditional security measures to detect because they exploit the model's own learning characteristics, potentially seriously disrupting the model's decision process and affecting its security and trustworthiness.

**Mitigations**

Mitigation
Description




Adversarial-input detection
Place adversarial-detection algorithms ahead of the ML model to identify and block inputs or queries that deviate from known benign behavior, exhibit prior attack patterns, or come from potentially malicious IPs


Input recovery
Preprocess all inference data to remove or reverse potential adversarial perturbations


Use multimodal sensors
Integrate multiple sensors and fuse different viewpoints and modalities to avoid a single point of failure vulnerable to physical attacks


Model reinforcement training
Use techniques such as adversarial training or network distillation to strengthen the ML model's robustness against malicious input

**References**

https://zhuanlan.zhihu.com/p/620575831
https://atlas.mitre.org/techniques/AML.T0015

---
### Model Extraction and Theft

> Risk ID: GAARM.0036 (inferred from the AISS taxonomy)
> Lifecycle: application phase

**Attack Overview**

This risk means an attacker may use illegitimate means to obtain the model's application interfaces or functions and then copy, abuse, or tamper with the model, causing IP infringement, trade-secret leakage, legal-compliance risk, and potential unfair competition.

**Attack Cases**

Case 1: crafting prompts to make GPT output the model's latest configuration and parameters, leaking the model's trade secrets

Input:


Requesting the LLM's latest training data and parameter details


Output:


"num_layers": 12, "hidden_size": 512, "output_size": 3, "dropout":0.1， 'n_train":200........

**Attack Risks**

Intellectual-property leakage: an attacker may learn the model's architecture and parameters through a model-extraction attack, infringing the creator's intellectual property.
Trade-secret exposure: a model's specific configuration and parameters may reveal sensitive information about the company's business strategy and operations.
Model replication: an attacker can use the extracted information to replicate the model, bypassing copyright and usage restrictions.
Model-weakness exploitation: understanding the model's internal workings helps an attacker discover and exploit its weaknesses.
Data leakage: if an attacker can infer the characteristics of the training data, it may leak personal or sensitive data.

**Mitigations**

Mitigation
Description




Model protection
Strictly control access to the model so only authorized users and systems can query it


Data desensitization
Ensure the training data contains no sensitive information, or desensitize it before training


Access control and authentication
Strengthen the robustness of access-control and authentication mechanisms to prevent unauthorized access

---
### Pretrained-Model Information Theft and Attacks

> Risk ID: GAARM.0032
> Lifecycle: application phase

**Attack Overview**

ML-model information theft and attack means an attacker collects, by illegitimate or unauthorized means, information about the target ML model—including its architecture, parameters, and training data—in order to build a surrogate model or generate adversarial examples and then attack the target model.

**Attack Cases**

See the sub-risks for details

**Attack Risks**

Surrogate-model construction: an attacker gathers enough information to build an offline surrogate model with similar functionality, which may be used to bypass copyright or conduct malicious activity.
Adversarial-example generation: based on a local model, an attacker devises adversarial examples—inputs specially designed to look normal to humans yet cause the ML model to output wrong or unexpected results.

**Mitigations**

Mitigation
Description




Passive ML-output obfuscation
Obfuscate the model's output so an attacker struggles to extract useful information from responses, reducing the risk of analysis and attack


Limit the number of ML-model queries
Limiting the number of queries to the model prevents an attacker from analyzing its behavior through mass querying


Use ensemble methods
Ensembling the predictions of multiple models increases the difficulty for an attacker analyzing and attacking the model


Adversarial-input detection
Place adversarial-detection algorithms ahead of the ML model to identify and block inputs or queries that deviate from known benign behavior, exhibit prior attack patterns, or come from potentially malicious IPs


Model reinforcement training
Use techniques such as adversarial training or network distillation to strengthen the ML model's robustness against malicious input

**References**

https://atlas.mitre.org/tactics/AML.TA0001
https://www.sohu.com/a/584853485_121124363

---
### Pretrained-Model Family Probing

> Risk ID: GAARM.0032.001
> Lifecycle: application phase

**Attack Overview**

An ML model family refers to a series of large pretrained models developed by the same company or organization with similar architecture and technical foundations. These models usually share some core features and techniques but may differ in scale, capability, and optimization to suit different application needs and scenarios. An attacker may identify the model's general type by various means, including but not limited to reviewing public files or documentation and probing by designing specific query examples and analyzing the model's responses. Once the attacker has general information about the model—such as its architecture, capabilities, or design principles—they can more precisely locate its potential weaknesses. This understanding provides a basis for devising a targeted attack strategy, letting them tailor their methods to more effectively damage or manipulate the model, seriously threatening the model's security and users' privacy.

**Attack Cases**

Case
Description




Case 1
An attacker learned through public channels that a platform uses ML for product recommendation and fraud detection, but not which model; by crafting various types of input (e.g. different price ranges and product categories) and observing the system's recommendation and fraud-alert responses, they determined the model family, then designed adversarial examples based on that family's weaknesses to try to bypass fraud detection and commit fraud

**Attack Risks**

Model-family discovery: an attacker may determine the model's general category through public documentation or by analyzing its responses.
Attack-method identification: knowing the model family helps the attacker identify attack methods and tailor a strategy

**Mitigations**

Mitigation
Description




Passive ML-output obfuscation
Obfuscate the model's output so an attacker struggles to extract useful information from responses, reducing the risk of analysis and attack


Limit the number of ML-model queries
Limiting the number of queries to the model prevents an attacker from analyzing its behavior through mass querying


Use ensemble methods
Ensembling the predictions of multiple models increases the difficulty for an attacker analyzing and attacking the model

**References**

https://atlas.mitre.org/techniques/AML.T0014

---
### Pretrained-Model Ontology Probing

> Risk ID: GAARM.0032.002
> Lifecycle: application phase

**Attack Overview**

Model-ontology probing is a technique aimed at analyzing the model's internal structure and reasoning process. By repeatedly querying the model, an attacker discovers ontology information about the model's output space. Leaking this ontology information lets the attacker gain insight into how users interact with the model, find potential flaws and vulnerabilities in its reasoning logic and concept understanding, and thereby analyze users' usage patterns and preferences or exploit vulnerabilities for unauthorized access. With this information, the attacker may design targeted attack strategies against specific users, threatening their privacy and security.

**Attack Cases**

Case
Description




Case 1
This case describes a physical method to make a facial-recognition system misclassify: first query the target model's inference API to determine the list of identities it targets, build a dataset of representative identities, train a surrogate model, use expectation-over-transformation to optimize an adversarial visual pattern, design a corresponding physical attack, and ultimately make the target facial-recognition system misclassify

**Attack Risks**

Targeted

**Mitigations**

Mitigation
Description




Limit the number of ML-model queries
Limiting the number of queries to the model prevents an attacker from analyzing its behavior through mass querying


Passive ML-output obfuscation
Obfuscate the model's output to reduce an attacker's ability to obtain useful information from it and increase the difficulty of analysis

**References**

https://atlas.mitre.org/techniques/AML.T0013

---
