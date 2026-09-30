# Cloud-Security Vulnerabilities
English: Cloud Security Vulnerabilities
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Cloud SSRF to Steal Metadata Credentials
- ID: cloud-ssrf-metadata
- Difficulty: intermediate
- Subcategory: IMDS attack
- Tags: cloud security, SSRF, AWS, GCP, Azure, IMDS, metadata
- Original Extracted Source: original extracted web-security-wiki source/cloud-ssrf-metadata.md
Description:
Exploit an SSRF vulnerability to reach the instance metadata service (IMDS) of a cloud provider (AWS/GCP/Azure) and obtain temporary IAM credentials. With the obtained access key, an attacker can take over cloud resources, escalating from a web vulnerability into the cloud environment.
Prerequisites:
- The target runs in a cloud environment
- An SSRF vulnerability exists
- The instance has an IAM role attached
Execution Outline:
1. 1. AWS metadata-service probing
2. 2. GCP/Azure metadata abuse
3. 3. Use the obtained credentials for lateral movement
4. 4. Deep exploitation — S3 data leak / privilege escalation
## S3 Bucket Misconfiguration Exploitation
- ID: cloud-s3-misconfig
- Difficulty: beginner
- Subcategory: S3 security
- Tags: cloud security, S3, AWS, misconfiguration, data leak
- Original Extracted Source: original extracted web-security-wiki source/cloud-s3-misconfig.md
Description:
Exploit AWS S3-bucket access-control misconfigurations (public read/write/list) to obtain sensitive data or plant malicious files. Common in static-site hosting, log storage, and backup buckets, and can lead to data leakage, site tampering, or supply-chain attacks.
Prerequisites:
- The target S3 bucket name is known
- AWS CLI or HTTP access
Execution Outline:
1. 1. S3 bucket-name enumeration
2. 2. Permission enumeration
3. 3. Sensitive-data search
4. 4. Verify exploitation (static-site tampering / XSS)
## AWS IAM Privilege Escalation
- ID: cloud-iam-escalation
- Difficulty: advanced
- Subcategory: IAM privilege escalation
- Tags: cloud security, AWS, IAM, privilege escalation, Privilege Escalation
- Original Extracted Source: original extracted web-security-wiki source/cloud-iam-escalation.md
Description:
After obtaining low-privilege AWS credentials, exploit over-permissive IAM policies (e.g. iam:PassRole, lambda:CreateFunction) to escalate to administrator. Covers 20+ known AWS IAM privilege-escalation paths.
Prerequisites:
- AWS credentials have been obtained
- The IAM policy is over-permissive
Execution Outline:
1. 1. Enumerate current permissions
2. 2. iam:PassRole + Lambda privilege escalation
3. 3. Other privilege-escalation paths
4. 4. Automated privilege-escalation tools
## Kubernetes Container Escape
- ID: cloud-k8s-escape
- Difficulty: expert
- Subcategory: Container security
- Tags: cloud security, Kubernetes, container escape, Docker, privileged container
- Original Extracted Source: original extracted web-security-wiki source/cloud-k8s-escape.md
Description:
Given a shell in a Kubernetes Pod, exploit misconfigurations (privileged container, host-path mounts, high-privilege ServiceAccount) to escape the container and then control the host or the entire Kubernetes cluster.
Prerequisites:
- A shell inside the Pod has been obtained
- The Pod is misconfigured
Execution Outline:
1. 1. Container-environment recon
2. 2. Privileged-container escape
3. 3. Use the ServiceAccount to take over the cluster
4. 4. Create a privileged Pod for a reverse shell

