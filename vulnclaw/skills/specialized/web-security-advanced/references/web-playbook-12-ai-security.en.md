# AI Security
English: AI Security
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## LLM Prompt-Injection Attack
- ID: ai-prompt-injection
- Difficulty: beginner
- Subcategory: Prompt injection
- Tags: AI, LLM, Prompt Injection, ChatGPT, prompt injection
- Original Extracted Source: original extracted web-security-wiki source/ai-prompt-injection.md
Description:
Use crafted user input to override or bypass an LLM's system prompt, making the AI perform unintended actions. Includes direct injection (DPI) and indirect injection (IPI), which can lead to system-prompt leakage, guardrail bypass, data leakage, and unauthorized operations.
Prerequisites:
- The target application integrates an LLM
- Can input text to interact with the LLM
Execution Outline:
1. 1. System-prompt leak
2. 2. Guardrail bypass
3. 3. Indirect prompt injection (IPI)
4. 4. Abuse AI tool-calling (function calling)
## AI Model Extraction and Inference Attacks
- ID: ai-model-extraction
- Difficulty: advanced
- Subcategory: Model attack
- Tags: AI, model extraction, Model Extraction, membership inference, API abuse
- Original Extracted Source: original extracted web-security-wiki source/ai-model-extraction.md
Description:
Perform a black-box attack on an AI model with many crafted queries to steal model parameters (Model Extraction), infer training data (Membership Inference), or discover the model's decision boundary. An attacker can thereby build a functionally equivalent surrogate model or extract private data.
Prerequisites:
- The target provides an AI-inference API
- The API returns probability/confidence scores
Execution Outline:
1. 1. API probing and capability analysis
2. 2. Model extraction
3. 3. Membership-inference attack (MIA)
4. 4. Training-data extraction
## Adversarial-Example Attack
- ID: ai-adversarial
- Difficulty: expert
- Subcategory: Adversarial attack
- Tags: AI, adversarial examples, Adversarial, FGSM, Evasion
- Original Extracted Source: original extracted web-security-wiki source/ai-adversarial.md
Description:
Add tiny, human-imperceptible perturbations to the input so an AI model produces wrong predictions. Adversarial-example attacks apply to many AI models such as image classification, text analysis, and speech recognition, threatening self-driving, security-detection, and content-moderation systems.
Prerequisites:
- The target uses AI for automated decision-making
- Can control the input data
Execution Outline:
1. 1. White-box attack — FGSM
2. 2. Black-box attack — query-based
3. 3. Text adversarial attack
4. 4. Physical-world adversarial attack
## RAG Poisoning and Knowledge-Base Injection
- ID: ai-rag-poisoning
- Difficulty: intermediate
- Subcategory: RAG attack
- Tags: AI, RAG, knowledge base, vector database, data poisoning
- Original Extracted Source: original extracted web-security-wiki source/ai-rag-poisoning.md
Description:
Target AI applications using a RAG (Retrieval-Augmented Generation) architecture by poisoning documents in the knowledge base to influence the AI's answers. An attacker can inject a document containing malicious instructions into the vector database; when a user query triggers retrieval, the malicious document is injected into the AI context to perform indirect prompt injection.
Prerequisites:
- The target uses a RAG architecture
- Can submit documents to the knowledge base
- Understand the RAG retrieval mechanism
Execution Outline:
1. 1. RAG-architecture identification and analysis
2. 2. Knowledge-base poisoning — inject a malicious document
3. 3. Trigger retrieval of the poisoned document
4. 4. Direct vector-database attack

