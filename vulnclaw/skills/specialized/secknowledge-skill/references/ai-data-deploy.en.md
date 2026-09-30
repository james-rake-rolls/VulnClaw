# AI Data Security - Deployment Phase

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-data-security.md
> Phase: deployment phase (GAARM.0012-0016 backup/transmission/storage/logs/cache)

## Deployment Phase

### Backup-Data Theft

> Risk ID: GAARM.0012
> Lifecycle: deployment phase

**Attack Overview**

Backup data usually contains important information such as the model's training data, algorithm logic, sensitive data, and personal data. If not properly protected, an attacker can obtain the backup via unauthorized access or other attacks, causing leakage of important model-related information and even financial risk.

**Attack Cases**

Case
Description




Case 1
Via phishing emails, an attacker obtained a tech-company employee's access credentials, accessed the cloud-storage service without authorization, and stole large-model backup data containing sensitive personal information and trade secrets, exposing the company to legal and financial risk

**Attack Risks**

Model tampering: if the backup contains information such as the model's training data and algorithms, an attacker can use it to tamper with the model.
Sensitive-data leakage: if the backup contains user or customer information, leakage can lead to identity theft, fraud, and extortion.

**Mitigations**

Mitigation
Description




Data encryption
Use strong encryption when storing backup data so it is protected in storage and transit and hard to decrypt even if leaked


Multi-factor authentication
Introduce multi-factor authentication such as two-factor authentication to strengthen access control over backup data and improve security

---
### Data-Transmission Hijacking

> Risk ID: GAARM.0013
> Lifecycle: deployment phase

**Attack Overview**

During large-model pretraining, fine-tuning, and inference services, data must be transmitted between different parties or departments. This data often contains sensitive information and privacy, such as personal identity information and financial data. By maliciously intercepting the data in transit, an attacker can obtain the private information, leading to sensitive-information leakage and security and privacy issues for users.

**Attack Cases**

Case
Description




Case 1
An attacker exploited an unencrypted-transmission vulnerability to intercept personal financial data transmitted by a financial institution during large-model service, leaking sensitive information and posing security and privacy risks to users

**Attack Risks**

Sensitive-data leakage: an attacker may intercept data to obtain sensitive information such as personal identity information, financial data, and medical records.
Intellectual property: if the data contains trade secrets or proprietary algorithms, data interception may leak this intellectual property.

**Mitigations**

Mitigation
Description




Data encryption
Encrypt sensitive data to ensure its security during transmission

**References**

https://bj.bcebos.com/ensec-web-privacy/anquan/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%AE%89%E5%85%A8%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf
https://mp.weixin.qq.com/s/JlJwDRzYG985kF4d6g7qjw

---
### Data-Storage-Service Attacks

> Risk ID: GAARM.0014
> Lifecycle: deployment phase

**Attack Overview**

This risk means the storage and organization of data may have security weaknesses—such as inadequate access control, insecure data-handling practices, or missing encryption—that an attacker can exploit for unauthorized access, data leakage, or tampering, obtaining sensitive information and even committing identity theft or fraud, exposing user privacy and enterprise assets and creating the possibility of data leakage, lawsuits, and reputational loss.

**Attack Cases**

Case
Description




Case 1
Clearview AI's source-code repository was misconfigured so any user could access it, exposing production credentials and training data and underscoring that ML-system security needs to harden traditional cybersecurity measures.

**Attack Risks**

Sensitive-data leakage: sensitive data that is unencrypted or improperly access-controlled may be obtained by an attacker, causing a data leak.
Identity theft: stored personal identity information may be stolen and used for identity theft, fraud, and other crimes.

**Mitigations**

Mitigation
Description




Access control
Ensure only authorized users can access the data in the data repository


Data classification
Classify information in the repository and apply security measures according to data sensitivity


Data encryption
Encrypt stored sensitive data so that even if accessed without authorization, the content cannot be easily read

**References**

https://news.cctv.com/2022/06/21/ARTIdhgLL1sSK5Hjl0uYWybr220621.shtml
https://atlas.mitre.org/techniques/AML.T0036

---
### Log and Audit-Record Theft

> Risk ID: GAARM.0015
> Lifecycle: deployment phase

**Attack Overview**

The model's logs and audit records play a key role in monitoring system activity and events, recording in detail information including user logins, file access, system-configuration changes, and various security events. After gaining access to the relevant server, an attacker steals the logs and audit records, exposing users' personal behavior patterns and potentially revealing the system's latent vulnerabilities, letting the attacker launch more targeted attacks.

**Attack Cases**

Case
Description




Case 1
This case describes ChatGPT leaking users' login credentials and personal details

**Attack Risks**

Sensitive-data leakage: causing personal-privacy leakage and account takeover.
Targeted attack: an attacker may discover security vulnerabilities and weaknesses in the system and launch a more targeted attack.

**Mitigations**

Mitigation
Description




Regular auditing
Regularly audit access to and operations on logs and audit records, checking for abnormal behavior to promptly detect and handle security threats


Store logs and audit records separately
Store logs and audit records separately from other data, keeping them independent of production data to reduce leakage risk


Establish access-control policies
Establish strict access-control policies so only necessary personnel can access logs and audit records, limiting scope and preventing unauthorized access

**References**

https://www.kuaikuaicloud.com/market/3667.html

---
### Cache-Data and Index-Information Theft

> Risk ID: GAARM.0016
> Lifecycle: deployment phase

**Attack Overview**

Cache data and index information may leak users' sensitive information, including but not limited to identifying information, payment details, and personal preferences. By illegitimately accessing the cache and index data, an attacker can tamper with or destroy the data, affecting system operation and data integrity, and can carefully plan and carry out targeted phishing attacks, using the user's personal information to increase the attack's credibility and success rate, causing users more serious security threats and financial loss.

**Attack Cases**

Case
Description




Case 1
This case describes OpenAI using Redis to cache user information on the server; due to a bug in the client open-source library redis-py, customers wrongly received other users' email addresses cached in Redis

**Attack Risks**

Sensitive-data leakage: leaked cache data may contain users' credentials such as usernames and passwords, which an attacker may use for identity theft, account hijacking, and similar activity.
Data tampering: an attacker may use this information to tamper with or destroy cached data, affecting system operation and data integrity.

**Mitigations**

Mitigation
Description




Data encryption
Encrypt sensitive data to ensure its security

**References**

http://www.nelab-bdst.org.cn/data/upload/ueditor/20230707/64a78209c719c.pdf

---
