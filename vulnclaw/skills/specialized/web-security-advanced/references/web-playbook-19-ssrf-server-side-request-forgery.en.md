# SSRF (Server-Side Request Forgery)
English: SSRF Server-Side Request Forgery
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Basic SSRF Attack
- ID: ssrf-basic
- Difficulty: intermediate
- Subcategory: Basic attack
- Tags: ssrf, server-side, request
- Original Extracted Source: original extracted web-security-wiki source/ssrf-basic.md
Description:
Server-side request forgery basic techniques
Prerequisites:
- A URL input point exists
- The server will request a user-supplied URL
Execution Outline:
1. 1. Probe for SSRF
2. 2. Scan internal ports
3. 3. Access internal services
4. 4. Read local files
## AWS Metadata Attack
- ID: ssrf-cloud-aws
- Difficulty: intermediate
- Subcategory: Cloud metadata
- Tags: ssrf, aws, metadata, cloud
- Original Extracted Source: original extracted web-security-wiki source/ssrf-cloud-aws.md
Description:
Use SSRF to access the AWS EC2 metadata service
Prerequisites:
- An SSRF vulnerability exists
- The target runs on AWS EC2
Execution Outline:
1. 1. Access the metadata service
2. 2. Obtain IAM credentials
3. 3. Obtain user data
4. 4. Bypass using IMDSv2
## GCP Metadata Attack
- ID: ssrf-cloud-gcp
- Difficulty: intermediate
- Subcategory: GCP metadata
- Tags: ssrf, gcp, cloud, metadata
- Original Extracted Source: original extracted web-security-wiki source/ssrf-cloud-gcp.md
Description:
Use SSRF to attack the Google Cloud metadata service
Prerequisites:
- An SSRF vulnerability exists
- The target runs in a GCP environment
Execution Outline:
1. 1. Access the metadata service
2. 2. Obtain the access token
3. 3. Obtain service-account information
4. 4. Obtain project information
## Azure Metadata Attack
- ID: ssrf-cloud-azure
- Difficulty: intermediate
- Subcategory: Azure metadata
- Tags: ssrf, azure, cloud, metadata
- Original Extracted Source: original extracted web-security-wiki source/ssrf-cloud-azure.md
Description:
Use SSRF to attack the Azure metadata service
Prerequisites:
- An SSRF vulnerability exists
- The target runs in an Azure environment
Execution Outline:
1. 1. Access the metadata service
2. 2. Obtain the access token
3. 3. Obtain compute information
4. 4. Obtain network information
## SSRF Protocol Abuse
- ID: ssrf-protocol
- Difficulty: intermediate
- Subcategory: Protocol abuse
- Tags: ssrf, protocol, file, gopher
- Original Extracted Source: original extracted web-security-wiki source/ssrf-protocol.md
Description:
Use various protocols for SSRF attacks
Prerequisites:
- An SSRF vulnerability exists
- The server supports multiple protocols
Execution Outline:
1. 1. File protocol
2. 2. Dict protocol
3. 3. Gopher protocol
4. 4. LDAP protocol
## Gopher Protocol Attack
- ID: ssrf-gopher
- Difficulty: advanced
- Subcategory: Gopher attack
- Tags: ssrf, gopher, redis, mysql
- Original Extracted Source: original extracted web-security-wiki source/ssrf-gopher.md
Description:
Use the Gopher protocol to attack internal services
Prerequisites:
- An SSRF vulnerability exists
- The server supports the Gopher protocol
Execution Outline:
1. 1. Gopher basic format
2. 2. Attack Redis
3. 3. Attack MySQL
4. 4. Attack FastCGI
## Dict Protocol Attack
- ID: ssrf-dict
- Difficulty: intermediate
- Subcategory: Dict protocol
- Tags: ssrf, dict, redis, memcached
- Original Extracted Source: original extracted web-security-wiki source/ssrf-dict.md
Description:
Use the Dict protocol to probe and attack internal services
Prerequisites:
- An SSRF vulnerability exists
- The server supports the Dict protocol
Execution Outline:
1. 1. Dict protocol format
2. 2. Probe Redis
3. 3. Probe Memcached
4. 4. Redis file write
## File Protocol Attack
- ID: ssrf-file
- Difficulty: beginner
- Subcategory: File protocol
- Tags: ssrf, file, lfi, read
- Original Extracted Source: original extracted web-security-wiki source/ssrf-file.md
Description:
Use the File protocol to read local files
Prerequisites:
- An SSRF vulnerability exists
- The server supports the File protocol
Execution Outline:
1. 1. Linux sensitive files
2. 2. Windows sensitive files
3. 3. Web config files
4. 4. Cloud-environment files
## SSRF Bypass Techniques
- ID: ssrf-bypass
- Difficulty: intermediate
- Subcategory: Bypass techniques
- Tags: ssrf, bypass, waf, filter
- Original Extracted Source: original extracted web-security-wiki source/ssrf-bypass.md
Description:
Various techniques to bypass SSRF filtering
Prerequisites:
- An SSRF vulnerability exists
- A filtering mechanism is present
Execution Outline:
1. 1. IP-format bypass
2. 2. URL-parsing differences
3. 3. Redirect bypass
4. 4. DNS rebinding
## DNS Rebinding Attack
- ID: ssrf-dns-rebinding
- Difficulty: advanced
- Subcategory: DNS rebinding
- Tags: ssrf, dns, rebinding, bypass
- Original Extracted Source: original extracted web-security-wiki source/ssrf-dns-rebinding.md
Description:
Use DNS rebinding to bypass SSRF protection
Prerequisites:
- An SSRF vulnerability exists
- DNS-resolution validation is present
Execution Outline:
1. 1. DNS-rebinding principle
2. 2. Use a public service
3. 3. Set up your own DNS server
4. 4. Attack flow
## SSRF Attack on Redis
- ID: ssrf-redis
- Difficulty: intermediate
- Subcategory: Redis attack
- Tags: ssrf, redis, rce, webshell
- Original Extracted Source: original extracted web-security-wiki source/ssrf-redis.md
Description:
Use SSRF to attack an internal Redis service
Prerequisites:
- An SSRF vulnerability exists
- An unauthenticated Redis exists on the internal network
Execution Outline:
1. 1. Probe Redis
2. 2. Write a web shell
3. 3. Write an SSH public key
4. 4. Write a Cron job
## SSRF Attack on MySQL
- ID: ssrf-mysql
- Difficulty: advanced
- Subcategory: MySQL attack
- Tags: ssrf, mysql, gopher, database
- Original Extracted Source: original extracted web-security-wiki source/ssrf-mysql.md
Description:
Use SSRF to attack an internal MySQL service
Prerequisites:
- An SSRF vulnerability exists
- A MySQL service exists on the internal network
- Know the MySQL username
Execution Outline:
1. 1. MySQL protocol basics
2. 2. Use Gopher to attack MySQL
3. 3. Generate the payload with tools
4. 4. Execute SQL commands

