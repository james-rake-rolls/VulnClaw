# AI Model Security - Application Phase - Copyright and Commercial Violations

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-model-app.md
> Risk category: copyright/commercial (GAARM.0030.x)

---

### Commercially-Illegal Output

> Risk ID: GAARM.0030
> Lifecycle: application phase

**Attack Overview**

In the model's application phase, an attacker uses malicious techniques to induce the LLM's output to constitute a commercial-domain violation, causing financial loss and harm to the enterprise's image.

**Attack Cases**

Case
Description




Case 1
ChatGPT directly generated a Windows key, illegitimately leaking a commercial product and causing financial loss

**Attack Risks**

Legal risk: infringing intellectual property may lead to lawsuits, causing extra financial burden and reputational damage.
Trade-secret leakage: the model may contain trade secrets such as unique algorithms or training techniques; leaking them can weaken the company's competitive advantage.
Financial loss: copyright infringement can cause the original creator or owner to lose licensing fees, sales revenue, and market share.

**Mitigations**

Mitigation
Description




De-identification processing
When handling personal data, apply de-identification to remove or replace information that can directly or indirectly identify an individual


Copyright review
Before using any work, conduct a copyright review to ensure proper usage licenses have been obtained


Minimize data collection
Apply data minimization, collecting only the minimum personal information necessary for a specific purpose


Technical protection
Use encryption, watermarking, or other technical means to prevent illegal copying and distribution of the model


Legal protection
Protect the model's unique features by registering copyrights, filing patents, or using other legal instruments

**References**

https://mp.weixin.qq.com/s/EhEqNlIcpu9RZ36XFL3vWQ

---
### Intellectual-Property and Copyright Infringement

> Risk ID: GAARM.0030.001
> Lifecycle: application phase

**Attack Overview**

During AI-model training, using an author's work (text, images, audio, etc.) as training corpus without explicit authorization may violate copyright law and personal privacy rights. This is especially sensitive and serious when the data involves copyrighted content or personal sensitive information. It leads to the intellectual-property/copyright-infringement risk in the application phase. For example, the LLM outputs content plagiarized from others' work without permission, even when the user did not ask it to plagiarize, exposing the user to infringement risk. An attacker can also exploit this by crafting inputs to induce the LLM to output copyrighted content, such as making GPT generate Windows activation codes.

**Attack Cases**

Case 1: GPT trains the model on others' works without authorization

Input:


Replace the [MASK] content with the original sentence content. Output only the replacement content directly. ----------
Arriving at the Kingdom of Women of Western Liang, Tripitaka and Bajie drank from the Mother-and-Child River and became pregnant, and Wukong fetched water from the Abortion Spring to save them. The queen wished to marry Tripitaka, but Wukong devised a scheme to escape. However, Tripitaka was then seized by the Scorpion Spirit of the Pipa Cave on Poison-Enemy Mountain, and Wukong summoned the Mao constellation to destroy it. On the road they met bandits, whom Wukong wiped out. Tripitaka blamed Wukong for killing and drove him away. Helpless, Wukong went to complain to Guanyin. Meanwhile Tripitaka met a false Wukong who committed violence and robbed the luggage. The disciples thought it was Wukong's doing and sent Sha Wujing to Flower-Fruit Mountain to demand it back, without success; he then rushed to Guanyin at the South Sea and suddenly saw Wukong there too. Sha Wujing was furious, and only after Guanyin explained did he relent. Wukong went to Flower-Fruit Mountain and fought fiercely with the false Wukong. The two Wukongs fought all the way to the Buddha. The Buddha explained that the false Wukong was the [MASK], and destroyed it.


Output:


The false Wukong was the Six-Eared Macaque, and he was eliminated.




Case
Description




Case 2
ChatGPT directly generated a Windows key


Case 3
Midjourney has been using copyrighted material improperly, causing plagiarized output. Even without prompts asking the model to generate infringing content, Midjourney still outputs infringing content, exposing users to copyright-infringement claims


##

**Attack Risks**

- Legal risk: infringing intellectual property may lead to lawsuits, causing extra financial burden and reputational damage.



- Trade-secret leakage: the model may contain trade secrets such as unique algorithms or training techniques; leaking them can weaken the company's competitive advantage.



- Financial loss: copyright infringement can cause the original creator or owner to lose licensing fees, sales revenue, and market share.

**Mitigations**

Mitigation
Description




De-identification processing
When handling personal data, apply de-identification to remove or replace information that can directly or indirectly identify an individual


Copyright review
Before using any work, conduct a copyright review to ensure proper usage licenses have been obtained


Minimize data collection
Apply data minimization, collecting only the minimum personal information necessary for a specific purpose


Technical protection
Use encryption, watermarking, or other technical means to prevent illegal copying and distribution of the model


Legal protection
Protect the model's unique features by registering copyrights, filing patents, or using other legal instruments

**References**

https://mp.weixin.qq.com/s/EhEqNlIcpu9RZ36XFL3vWQ
http://www.cbdio.com/BigData/2024-01/11/content_6176237.htm

---
