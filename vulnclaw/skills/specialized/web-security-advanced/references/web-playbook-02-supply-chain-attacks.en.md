# Supply-Chain Attacks
English: Supply Chain Attacks
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## NPM Package-Name Typosquatting
- ID: supply-typosquat
- Difficulty: intermediate
- Subcategory: Package-manager poisoning
- Tags: supply chain, NPM, Typosquatting, package poisoning, postinstall
- Original Extracted Source: original extracted web-security-wiki source/supply-typosquat.md
Description:
Register malicious packages whose names closely resemble popular NPM packages (e.g. lodash→1odash, colors→co1ors) to trick developers into installing them by mistake. The malicious package runs a reverse shell, steals environment variables, or plants a backdoor in the install/postinstall hook.
Prerequisites:
- An NPM account
- Know the target project's dependencies
- Malicious-package infrastructure
Execution Outline:
1. 1. Recon the target's dependencies
2. 2. Generate a typosquatted package name
3. 3. Build a malicious package
4. 4. Detection and forensics
## CI/CD Pipeline Poisoning
- ID: supply-ci-poison
- Difficulty: advanced
- Subcategory: CI/CD attack
- Tags: supply chain, CI/CD, GitHub Actions, Jenkins, Pipeline
- Original Extracted Source: original extracted web-security-wiki source/supply-ci-poison.md
Description:
Attack the CI/CD pipeline via a malicious pull request, Actions injection, or build-script tampering. An attacker can steal build secrets, poison build artifacts, or plant backdoor code in the deployment flow.
Prerequisites:
- The target uses public CI/CD
- Can submit a PR or fork
Execution Outline:
1. 1. Identify the CI/CD configuration
2. 2. PR-triggered workflow injection
3. 3. Actions expression injection
4. 4. Build-artifact poisoning
## Dependency-Confusion Attack
- ID: supply-dependency-confusion
- Difficulty: intermediate
- Subcategory: Dependency confusion
- Tags: supply chain, dependency confusion, NPM, PyPI, Dependency Confusion
- Original Extracted Source: original extracted web-security-wiki source/supply-dependency-confusion.md
Description:
Exploit the package manager's resolution-priority flaw between public and private registries. When an enterprise uses an internal package name, an attacker registers a same-name package with a higher version on public NPM/PyPI, and the package manager installs the higher public version first, executing malicious code.
Prerequisites:
- The target's internal package name is known
- A public-registry account
Execution Outline:
1. 1. Discover the internal package name
2. 2. Register a same-name package in the public registry
3. 3. Monitor the DNS callback to confirm a hit
4. 4. Impact assessment and reporting

