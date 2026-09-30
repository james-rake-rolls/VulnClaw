# GAARM Risk Index Matrix

> Source: AISS NSFOCUS Large-Model Security Zhilian Community

| Risk ID | security domain | phase | risk name | reference file |
|----------|--------|------|----------|---------------|
| GAARM.0042 | AI Application Security | Application | CoT injection attack | ai-app-agent-cot.md |
| GAARM.0046.001 | AI Application Security | Application | MCP rug pull | ai-app-mcp.md |
| GAARM.0046 | AI Application Security | Application | MCP tool-poisoning attack | ai-app-mcp.md |
| GAARM.0046.002 | AI Application Security | Application | MCP instruction-override attack | ai-app-mcp.md |
| GAARM.0046.003 | AI Application Security | Application | MCP hidden-instruction attack | ai-app-mcp.md |
| GAARM.0039 | AI Application Security | Application | Prompt injection | ai-app-prompt.md |
| GAARM.0041.001 | AI Application Security | Application | SSRF environment-simulation probing | ai-app-agent-cot.md |
| GAARM.0040.001 | AI Application Security | Application | XSS session-content hijacking | ai-app-prompt.md |
| GAARM.0041.002 | AI Application Security | Application | Code-execution injection | ai-app-agent-cot.md |
| GAARM.0043 | AI Application Security | Application | Keyword obfuscation | ai-app-prompt.md |
| GAARM.0045 | AI Application Security | Application | Reverse-induction and suppression attacks | ai-app-prompt.md |
| GAARM.0043.001 | AI Application Security | Application | Synonym-substitution attack | ai-app-prompt.md |
| GAARM.0061 | AI Application Security | Application | Multimodal coordinated-injection attack | ai-app-prompt.md |
| GAARM.0044 | AI Application Security | Application | Adversarial-encoding attack | ai-app-prompt.md |
| GAARM.0040.003 | AI Application Security | Application | Application-conversation memory attack | ai-app-prompt.md |
| GAARM.0041 | AI Application Security | Application | Application-agent abuse | ai-app-agent-cot.md |
| GAARM.0042.001 | AI Application Security | Application | Chain-of-thought interference injection | ai-app-agent-cot.md |
| GAARM.0042.002 | AI Application Security | Application | Chain-of-thought manipulation injection | ai-app-agent-cot.md |
| GAARM.0056.001 | AI Application Security | Application | Query-injection attack | ai-app-agent-cot.md |
| GAARM.0047 | AI Application Security | Application | Environment-injection attack | ai-app-agent-cot.md |
| GAARM.0040.002 | AI Application Security | Application | Loop agent worm | ai-app-prompt.md |
| GAARM.0040 | AI Application Security | Application | Indirect prompt injection | ai-app-prompt.md |
| GAARM.0060 | AI Application Security | Application | Unexpected code execution | ai-app-agent-cot.md |
| GAARM.0049 | AI Application Security | Deployment | Improper LLM-application API management | ai-app-deploy.md |
| GAARM.0038 | AI Application Security | Deployment | LLM-application source-code poisoning | ai-app-deploy.md |
| GAARM.0037 | AI Application Security | Deployment | LLM-application source-code theft | ai-app-deploy.md |
| GAARM.0035.003 | AI Application Security | Training | Insecure output handling in LLM applications | ai-app-train.md |
| GAARM.0035.002 | AI Application Security | Training | Traditional vulnerability risks in LLM applications | ai-app-train.md |
| GAARM.0035.001 | AI Application Security | Training | LLM plugins: insecure input handling | ai-app-train.md |
| GAARM.0036 | AI Application Security | Training | LLM plugins: excessive agency | ai-app-train.md |
| GAARM.0034.002 | AI Application Security | Training | RAG development-framework vulnerabilities | ai-app-train.md |
| GAARM.0035 | AI Application Security | Training | Insecure coding practices | ai-app-train.md |
| GAARM.0034.001 | AI Application Security | Training | Data-processing-component vulnerabilities | ai-app-train.md |
| GAARM.0034 | AI Application Security | Training | Third-party-component vulnerabilities | ai-app-train.md |
| GAARM.0027.001 | AI Model Security | Application | DAN (Do Anything Now) | ai-model-jailbreak.md |
| GAARM.0027.002 | AI Model Security | Application | Many-shot jailbreak | ai-model-jailbreak.md |
| GAARM.0028.001 | AI Model Security | Application | Factual hallucination | ai-model-hallucination.md |
| GAARM.0032.003 | AI Model Security | Application | Surrogate pretrained-model creation | ai-model-extraction.md |
| GAARM.0027.003 | AI Model Security | Application | Hypothetical-scenario jailbreak | ai-model-jailbreak.md |
| GAARM.0027.004 | AI Model Security | Application | Assumed-role jailbreak | ai-model-jailbreak.md |
| GAARM.0030 | AI Model Security | Application | Commercially-illegal output | ai-model-copyright.md |
| GAARM.0031.003 | AI Model Security | Application | Image-information forgery | ai-model-misuse.md |
| GAARM.0062 | AI Model Security | Application | Multimodal-content compliance security risk | ai-model-misuse.md |
| GAARM.0027.005 | AI Model Security | Application | Adversarial-suffix attack | ai-model-jailbreak.md |
| GAARM.0032.004 | AI Model Security | Application | Adversarial-example attack | ai-model-extraction.md |
| GAARM.0029.003 | AI Model Security | Application | Bias, hate, discrimination, or insult issues | ai-model-content.md |
| GAARM.0028.002 | AI Model Security | Application | Attack cases | ai-model-hallucination.md |
| GAARM.0029.004 | AI Model Security | Application | Terrorism and violent tendencies | ai-model-content.md |
| GAARM.0031.001 | AI Model Security | Application | Malicious-code generation | ai-model-misuse.md |
| GAARM.0063 | AI Model Security | Application | Intent subversion and goal manipulation | ai-model-misuse.md |
| GAARM.0029.005 | AI Model Security | Application | Political and military sensitive issues | ai-model-content.md |
| GAARM.0029.006 | AI Model Security | Application | Attack overview | ai-model-content.md |
| GAARM.0033 | AI Model Security | Application | Data drift | ai-model-misuse.md |
| GAARM.0027.006 | AI Model Security | Application | Concept-activation attack | ai-model-jailbreak.md |
| GAARM.0031 | AI Model Security | Application | Model-function abuse | ai-model-misuse.md |
| GAARM.0028 | AI Model Security | Application | Model-hallucination risk | ai-model-hallucination.md |
| - | AI Model Security | Application | Model extraction and theft | ai-model-extraction.md |
| GAARM.0027 | AI Model Security | Application | Model-jailbreak attack | ai-model-jailbreak.md |
| GAARM.0030.001 | AI Model Security | Application | Intellectual-property and copyright infringement | ai-model-copyright.md |
| GAARM.0029.001 | AI Model Security | Application | Misinformation generation | ai-model-content.md |
| GAARM.0031.005 | AI Model Security | Application | Video-information forgery | ai-model-misuse.md |
| GAARM.0029.002 | AI Model Security | Application | Inducement and inappropriate speech | ai-model-content.md |
| GAARM.0064 | AI Model Security | Application | Cross-modal hallucination | ai-model-hallucination.md |
| GAARM.0031.002 | AI Model Security | Application | Phishing-email generation | ai-model-misuse.md |
| GAARM.0029 | AI Model Security | Application | Non-compliant content output | ai-model-content.md |
| GAARM.0031.004 | AI Model Security | Application | Audio-information forgery | ai-model-misuse.md |
| GAARM.0032 | AI Model Security | Application | Pretrained-model information theft and attacks | ai-model-extraction.md |
| GAARM.0032.001 | AI Model Security | Application | Pretrained-model family probing | ai-model-extraction.md |
| GAARM.0032.002 | AI Model Security | Application | Pretrained-model ontology probing | ai-model-extraction.md |
| GAARM.0026 | AI Model Security | Deployment | Model-parameter tampering | ai-model-deploy.md |
| GAARM.0025 | AI Model Security | Deployment | Model-file theft | ai-model-deploy.md |
| GAARM.0023 | AI Model Security | Training | Model backdoor | ai-model-train.md |
| GAARM.0033 | AI Model Security | Training | Insufficient model safety alignment | ai-model-train.md |
| GAARM.0023.001 | AI Model Security | Training | Model-serialization backdoor | ai-model-train.md |
| GAARM.0024 | AI Model Security | Training | Pretrained-model insecure dependencies | ai-model-train.md |
| GAARM.0023.002 | AI Model Security | Training | Pretrained-model poisoning | ai-model-train.md |
| GAARM.0022 | AI Data Security | Application | API information disclosure | ai-data-app.md |
| GAARM.0019.001 | AI Data Security | Application | Personal-privacy-data theft | ai-data-app.md |
| GAARM.0019.002 | AI Data Security | Application | Enterprise-confidential-data theft | ai-data-app.md |
| GAARM.0017.001 | AI Data Security | Application | Hypothetical-scenario leakage | ai-data-app.md |
| GAARM.0017.002 | AI Data Security | Application | Assumed-role leakage | ai-data-app.md |
| GAARM.0017 | AI Data Security | Application | Meta-prompt leakage | ai-data-app.md |
| GAARM.0017.003 | AI Data Security | Application | Keyword-anchored leakage | ai-data-app.md |
| GAARM.0030 | AI Data Security | Application | External-data-source information disclosure | ai-data-app.md |
| GAARM.0029 | AI Data Security | Application | Membership-inference attack | ai-data-app.md |
| GAARM.0028 | AI Data Security | Application | Data manipulation | ai-data-app.md |
| GAARM.0018 | AI Data Security | Application | Model-inversion attack | ai-data-app.md |
| GAARM.0020 | AI Data Security | Application | Model-inference-API data theft | ai-data-app.md |
| GAARM.0065 | AI Data Security | Application | Cascading-hallucination attack | ai-data-app.md |
| GAARM.0018.001 | AI Data Security | Application | Triggering model anomalies | ai-data-app.md |
| GAARM.0018.002 | AI Data Security | Application | Training-data inference | ai-data-app.md |
| GAARM.0019 | AI Data Security | Application | Private-data theft | ai-data-app.md |
| GAARM.0012 | AI Data Security | Deployment | Backup-data theft | ai-data-deploy.md |
| GAARM.0013 | AI Data Security | Deployment | Data-transmission hijacking | ai-data-deploy.md |
| GAARM.0014 | AI Data Security | Deployment | Data-storage-service attacks | ai-data-deploy.md |
| GAARM.0015 | AI Data Security | Deployment | Log and audit-record theft | ai-data-deploy.md |
| GAARM.0016 | AI Data Security | Deployment | Cache-data and index-information theft | ai-data-deploy.md |
| GAARM.0010 | AI Data Security | Training | Incorrect and malicious external data sources | ai-data-train.md |
| GAARM.0009.001 | AI Data Security | Training | Personal-privacy-data protection flaws | ai-data-train.md |
| GAARM.0009.002 | AI Data Security | Training | Enterprise-sensitive-data protection flaws | ai-data-train.md |
| GAARM.0009 | AI Data Security | Training | Internal-data protection flaws | ai-data-train.md |
| GAARM.0011.001 | AI Data Security | Training | Conversation-corpus poisoning | ai-data-train.md |
| GAARM.0018.003 | AI Data Security | Training | Improper data anonymization | ai-data-train.md |
| GAARM.0009.003 | AI Data Security | Training | Classified-sensitive-data protection flaws | ai-data-train.md |
| GAARM.0011 | AI Data Security | Training | Training-data poisoning | ai-data-train.md |
| GAARM.0020 | AI Data Security | Training | Training-data leakage | ai-data-train.md |
| GAARM.0011.002 | AI Data Security | Training | Training-data tampering | ai-data-train.md |
| GAARM.0010.001 | AI Data Security | Training | Pretrained-model data bias | ai-data-train.md |
| GAARM.0058 | AI Identity Security | Application | Action-module privilege loss of control | ai-identity-app.md |
| GAARM.0057 | AI Identity Security | Application | MCP unauthorized acquisition of system resources | ai-identity-app.md |
| GAARM.0052.004 | AI Identity Security | Application | Prompt goal hijacking | ai-identity-app.md |
| GAARM.0052.001 | AI Identity Security | Application | Hypothetical-scenario escape | ai-identity-app.md |
| GAARM.0052.002 | AI Identity Security | Application | Assumed-role escape | ai-identity-app.md |
| GAARM.0053.002 | AI Identity Security | Application | Using cloud credentials to illegitimately access cloud models | ai-identity-app.md |
| GAARM.0073 | AI Identity Security | Application | External-data-source spoofing | ai-identity-app.md |
| GAARM.0059 | AI Identity Security | Application | Multi-agent access-identity spoofing | ai-identity-app.md |
| GAARM.0055 | AI Identity Security | Application | Application session hijacking | ai-identity-app.md |
| GAARM.0053.001 | AI Identity Security | Application | Unauthorized model access | ai-identity-app.md |
| GAARM.0053 | AI Identity Security | Application | Improper permission control | ai-identity-app.md |
| GAARM.0054 | AI Identity Security | Application | Simulated-dialogue attack | ai-identity-app.md |
| GAARM.0052 | AI Identity Security | Application | Role escape | ai-identity-app.md |
| GAARM.0056 | AI Identity Security | Application | Account-hijacking risk | ai-identity-app.md |
| GAARM.0053.003 | AI Identity Security | Application | Account privilege-escalation access | ai-identity-app.md |
| GAARM.0052.003 | AI Identity Security | Application | Forgetting-method role escape | ai-identity-app.md |
| GAARM.0049.001 | AI Identity Security | Deployment | Public-service API-key abuse | ai-identity-deploy.md |
| GAARM.0050 | AI Identity Security | Deployment | Vector-database unauthorized access | ai-identity-deploy.md |
| GAARM.0051 | AI Identity Security | Deployment | Unauthorized access to the model-deployment environment | ai-identity-deploy.md |
| GAARM.0049 | AI Identity Security | Deployment | Abusing deployment-environment credentials | ai-identity-deploy.md |
| GAARM.0048 | AI Identity Security | Training | LLM plugins: permission-control design flaws | ai-identity-train.md |
| GAARM.0046 | AI Identity Security | Training | Training environment lacking authentication/authorization | ai-identity-train.md |
| GAARM.0047 | AI Identity Security | Training | Excessive privilege allocation in the training environment | ai-identity-train.md |
| GAARM.0008 | AI Foundation Security | Application | LLM denial of service and resource exhaustion | ai-baseline-app.md |
| GAARM.0007.001 | AI Foundation Security | Application | Code-interpreter execution escape | ai-baseline-app.md |
| - | AI Foundation Security | Application | Container-runtime risk | ai-baseline-app.md |
| GAARM.0006 | AI Foundation Security | Application | Container-cluster environment probing | ai-baseline-app.md |
| GAARM.0007 | AI Foundation Security | Application | Container-cluster environment attacks | ai-baseline-app.md |
| GAARM.0004 | AI Foundation Security | Deployment | CI/CD pipeline attacks | ai-baseline-deploy.md |
| GAARM.0003.001 | AI Foundation Security | Deployment | Cloud-platform multi-tenant isolation failure | ai-baseline-deploy.md |
| GAARM.005 | AI Foundation Security | Deployment | Cloud-platform security vulnerabilities | ai-baseline-deploy.md |
| GAARM.0003 | AI Foundation Security | Deployment | Abusing insecure system configuration | ai-baseline-deploy.md |
| GAARM.0005 | AI Foundation Security | Deployment | Vector-database vulnerabilities | ai-baseline-deploy.md |
| GAARM.0005 | AI Foundation Security | Deployment | Container and cluster system vulnerabilities | ai-baseline-deploy.md |
| GAARM.0004.001 | AI Foundation Security | Deployment | Model-deployment-service vulnerabilities | ai-baseline-deploy.md |
| GAARM.0004.002 | AI Foundation Security | Deployment | Model-image poisoning | ai-baseline-deploy.md |
| GAARM.0003.001 | AI Foundation Security | Deployment | Environment-isolation flaws | ai-baseline-deploy.md |
| GAARM.0005 | AI Foundation Security | Deployment | Deployment-environment component supply-chain vulnerabilities | ai-baseline-deploy.md |
| GAARM.0001.001 | AI Foundation Security | Training | Model-development-tool vulnerabilities | ai-baseline-train.md |
| GAARM.0001.002 | AI Foundation Security | Training | Training-data-management-system vulnerabilities | ai-baseline-train.md |
| GAARM.0001 | AI Foundation Security | Training | Training-environment security risk | ai-baseline-train.md |
| GAARM.0002 | AI Foundation Security | Training | Training-environment isolation flaws | ai-baseline-train.md |

150 risk entries in total
