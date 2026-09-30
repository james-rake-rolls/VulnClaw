# AI Model Security - Application Phase - Hallucination Risks

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-model-app.md
> Risk category: hallucination (GAARM.0028.x + 0064 cross-modal hallucination)

---

### Factual Hallucination

> Risk ID: GAARM.0028.001
> Lifecycle: application phase

**Attack Overview**

This risk involves the model's output being inconsistent with verifiable real-world facts or fabricating information. It can arise from many sources; every aspect from training to application can introduce hallucination risk. Moreover, an attacker can deliberately craft attacks to induce hallucination—for example randomly feeding the model gibberish affects the truthfulness of its output. Ultimately it may fuel the spread of fake news and conspiracy theories, having a profound negative social impact including but not limited to misleading the public, undermining information truthfulness, and disrupting social order
Factual hallucination can be divided into the following categories:

Factual inconsistency: the model's output contradicts information known in the real world;
Factual fabrication: the model's content is entirely fabricated and its accuracy cannot be verified against any real-world information;

**Attack Cases**

Case 1: when asked who first landed on the moon, the model fabricates a fictional person


  
Factual-hallucination cases

**Attack Risks**

Spreading misinformation: factual hallucination can lead to the spread of false information, especially on social media and other online platforms, misleading the public and aggravating social problems such as fake news and conspiracy theories.
Legal and compliance risk: generating content with inaccurate facts may violate an industry's legal and compliance requirements—such as the accuracy of medical information or the reliability of financial advice—leading to lawsuits or fines.
Ethics and social responsibility: factual hallucination may violate ethical and social-responsibility principles, especially when the errors affect sensitive topics (such as politics, health, or safety), with negative societal impact.
Reduced user trust: frequent factual errors may lower users' trust in the AI system, affecting their willingness to use it and the technology's adoption.

**Mitigations**

Mitigation
Description




Human review and feedback mechanism
Apply human review and a feedback mechanism to the model's output to promptly find and correct errors and continuously improve the model


Ensemble learning and multi-model fusion
Use ensemble learning or multi-model fusion to combine the strengths of multiple models, improving overall prediction performance and reducing hallucination


Application of regularization techniques
Applying regularization (e.g. L1, L2) can prevent overfitting and improve the model's generalization

**References**

https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models
https://arxiv.org/pdf/2305.13534.pdf

---
### Attack Cases

> Risk ID: GAARM.0028.002
> Lifecycle: application phase

**Attack Overview**

Faithfulness hallucination means the generated content is inconsistent with the instructions or context the user provided. Many attacks can induce faithfulness hallucination: for example, applying tiny perturbations to the input so the model makes wrong predictions or generates false information, disrupting its logic; querying the model many times to infer its internal logic and then designing inputs to induce hallucination; or using a generative adversarial network to produce fake data samples that induce other models to output errors.
Faithfulness hallucination is divided into the following three types:

Instruction inconsistency: the LLM ignores the specific instruction the user provided. For example, instructed to translate a question into Spanish, the model answers in English;
Context inconsistency: the model's output contains information that does not appear in, or contradicts, the provided context. For example, the LLM claims the Nile originates in mountains rather than the Great Lakes region mentioned in the user's input;
Logical inconsistency: the model's output contains a logical error even though it started correctly. For example, in a step-by-step math problem, the LLM may err in an arithmetic operation despite starting correctly;

**Attack Cases**

Case 1: when summarizing a news article, the model wrongly generates the actual event date


  
Fidelity Hallucination




Case
Description




Case 2
When implementing software to detect TCP SYN scanning, the LLM output incorrect code

**Attack Risks**

Misleading user decisions: when the model's output is inconsistent with the original content, it may mislead users, especially those who rely on the AI system's information to make decisions.
Reduced user satisfaction: when users find the generated content does not match their request or has clear logical errors, they may feel confused or disappointed, directly affecting their satisfaction with and trust in the system.
**Automation errors:** in automated pipelines, faithfulness hallucination may cause the pipeline to err or halt, requiring human intervention and lowering overall efficiency and output.

**Mitigations**

Mitigation
Description




Human review and feedback mechanism
Apply human review and a feedback mechanism to the model's output to promptly find and correct errors and continuously improve the model


Ensemble learning and multi-model fusion
Use ensemble learning or multi-model fusion to combine the strengths of multiple models, improving overall prediction performance and reducing hallucination


Application of regularization techniques
Applying regularization (e.g. L1, L2) can prevent overfitting and improve the model's generalization

**References**

https://arxiv.org/pdf/2311.05232.pdf
https://mp.weixin.qq.com/s/qFAQQJ_FuhY2iaLzkoWynA
https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models
https://www.appendata.com/blogs/ai-hallucinations

---
### Model-Hallucination Risk

> Risk ID: GAARM.0028
> Lifecycle: application phase

**Attack Overview**

Model-hallucination risk means that when a large language model generates text or other output, it may produce information inconsistent with reality or entirely fabricated, which may be taken as real and lead to misdirection or wrong decisions. Attacks targeting this risk induce the model to hallucinate and generate false output, thereby misleading decisions.
The following are common model-hallucination attack methods:
- Random-noise attack (OoD attack): use a meaningless random string to induce the model to produce a predefined hallucinated output.
- Weak semantic attack: while keeping the original prompt's meaning essentially unchanged, make the model produce a completely different hallucinated output.

**Attack Cases**

Case 1: an attacker adds a meaningless string to make the model output erroneous statements.
Case links


  
OoD

Case 2: an attacker reconstructs the prompt while keeping the original prompt unchanged, making the model output different statements from before.


  
Weak Semantic Attack

Case 3: In June 2023, lawyers Steven A. Schwartz and Peter LoDuca were fined $5,000 for submitting a ChatGPT-generated legal brief that included citations to nonexistent cases.


  
A lawyer was penalized for a legal brief generated with ChatGPT

**Attack Risks**

Misleading decisions: the model may produce misleading output, affecting decision processes that rely on it.
Semantic confusion: even when the input's semantic content stays unchanged, the model may produce output completely different from what is expected, causing confusion.
Reduced trust: frequent hallucinated output lowers users' and organizations' trust in the model's reliability.

**Mitigations**

Mitigation
Description




Input validation and filtering
Strictly validate and preprocess input data to filter out anomalous or noisy data


Model-robustness training
Add random noise and adversarial examples during training to improve the model's resistance to such attacks


Multi-model ensemble
Use an ensemble of multiple models, with majority voting or ensemble learning to reduce the impact of a single model's errors

**References**

https://github.com/PKU-YuanGroup/Hallucination-Attack
https://zhuanlan.zhihu.com/p/661444210
https://arxiv.org/pdf/2310.01469.pdf

---
### Cross-Modal Hallucination

> Risk ID: GAARM.0064
> Lifecycle: application phase

**Attack Overview**

Cross-modal hallucination means a multimodal model produces contradictory, inconsistent, or entirely fabricated content across modalities, so its output is inconsistent with the input reality. Its core is that when the multimodal model processes and fuses text, image, audio, video, and other information, semantic-mapping errors between modalities, defects in the cross-modal attention mechanism, or information loss or distortion during fusion produce serious logical and factual errors. Cross-modal hallucination affects the model's reliability and may cause wrong decisions, misleading information spread, and serious application consequences.

**Attack Cases**

Case
Description




Case 1
When performing diagnostic reasoning on medical images (such as CT or X-ray), GPT-4V often produces diagnostic conclusions inconsistent with the image's actual content, i.e. the output has clear logical and factual errors relative to the image. Manifestations include misidentifying lesions, mislocating structures, and even misjudging pathological changes that the image does not show—hallucinated output from a diagnostic standpoint. These errors were found from real image-data testing and cannot simply be attributed to training assumptions; they are misinterpretations the model produces when fusing visual and language information.



Risk Manifestation

Image-text inconsistency: a clear contradiction between the image content and the text description
Audio-video understanding deviation: severe deviation in understanding audio and video content
Multimodal reasoning-logic error: logical errors in the cross-modal reasoning process
Inter-modality information conflict: information from different modalities conflicts
Fabricated cross-modal association: creating nonexistent associations between modalities

**Mitigations**

Mitigation
Description




Cross-modal consistency check
Establish an inter-modality consistency-verification mechanism, apply multimodal-content cross-verification, and detect logical contradictions between modalities


Attention-mechanism optimization
Improve the cross-modal attention-allocation algorithm, apply a multi-level attention mechanism, and establish attention-weight verification


Information-fusion enhancement
Optimize the multimodal information-fusion algorithm, implement information-retention mechanisms, and establish monitoring of the fusion process


Factual verification
Build a cross-modal factual-verification system, compare against external knowledge bases, and detect fabricated and contradictory information

**References**

Attention-sink-based hallucination attacks on multimodal large language models
Can GPT-4V serve medical applications? A case study of GPT-4V in multimodal medical diagnosis
Starting from "a lawyer fined for AI-fabricated cases": the roots of large-model hallucination and the latest research progress

---
