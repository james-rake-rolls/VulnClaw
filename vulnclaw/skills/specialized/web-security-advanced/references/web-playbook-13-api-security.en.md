# API Security
English: API Security
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## JWT Security Vulnerabilities
- ID: jwt-security
- Difficulty: intermediate
- Subcategory: JWT
- Tags: jwt, token, authentication
- Original Extracted Source: original extracted web-security-wiki source/jwt-security.md
Description:
JSON Web Token security-vulnerability exploitation
Prerequisites:
- Uses JWT for authentication
- There is an issue with the JWT configuration or validation
Execution Outline:
1. 1. Decode the JWT
2. 2. None-algorithm attack
3. 3. Weak-key cracking
4. 4. Key-confusion attack
## GraphQL Injection Attack
- ID: graphql-injection
- Difficulty: intermediate
- Subcategory: GraphQL
- Tags: graphql, api, injection, introspection
- Original Extracted Source: original extracted web-security-wiki source/graphql-injection.md
Description:
GraphQL API injection and information-disclosure attacks
Prerequisites:
- The target uses a GraphQL API
- An unauthorized-access or injection point exists
Execution Outline:
1. 1. Probe for the GraphQL endpoint
2. 2. Introspection query
3. 3. Batch-query attack
4. 4. SQL injection
## GraphQL Introspection Attack
- ID: graphql-introspection
- Difficulty: beginner
- Subcategory: GraphQL introspection
- Tags: graphql, introspection, enumeration, api
- Original Extracted Source: original extracted web-security-wiki source/graphql-introspection.md
Description:
Use GraphQL introspection to obtain the API structure
Prerequisites:
- The target uses GraphQL
- Introspection is not disabled
Execution Outline:
1. 1. Basic introspection
2. 2. Full introspection
3. 3. Analyze with tools
## GraphQL Batch-Query Attack
- ID: graphql-batching
- Difficulty: intermediate
- Subcategory: GraphQL batch query
- Tags: graphql, batching, rate-limit, bypass
- Original Extracted Source: original extracted web-security-wiki source/graphql-batching.md
Description:
Use GraphQL batch queries to bypass rate limiting
Prerequisites:
- The target uses GraphQL
- Rate limiting is present
Execution Outline:
1. 1. Alias batch query
2. 2. Array batch query
3. 3. Brute force
## REST API Security Testing
- ID: rest-api-security
- Difficulty: intermediate
- Subcategory: REST API
- Tags: rest, api, security, testing
- Original Extracted Source: original extracted web-security-wiki source/rest-api-security.md
Description:
REST API security testing and exploitation
Prerequisites:
- The target uses a REST API
- Know the API endpoints
Execution Outline:
1. 1. API-endpoint discovery
2. 2. Authentication test
3. 3. HTTP-method testing
4. 4. Parameter pollution
## JWT None-Algorithm Attack
- ID: jwt-none-alg
- Difficulty: beginner
- Subcategory: JWT security
- Tags: jwt, none, algorithm, bypass
- Original Extracted Source: original extracted web-security-wiki source/jwt-none-alg.md
Description:
Use the JWT None algorithm to bypass signature verification
Prerequisites:
- The target uses JWT authentication
- The server does not correctly validate the algorithm
Execution Outline:
1. 1. Decode the JWT
2. 2. Build a None-algorithm token
3. 3. Modify user permissions
4. 4. Send a malicious token
## JWT Key-Confusion Attack
- ID: jwt-key-confusion
- Difficulty: intermediate
- Subcategory: JWT security
- Tags: jwt, algorithm, confusion, rs256
- Original Extracted Source: original extracted web-security-wiki source/jwt-key-confusion.md
Description:
Use JWT algorithm confusion to bypass the signature
Prerequisites:
- The target uses the RS256 algorithm
- Can obtain the public key
Execution Outline:
1. 1. Obtain the public key
2. 2. Algorithm-confusion attack
3. 3. Send a malicious token
## IDOR (Insecure Direct Object Reference)
- ID: api-idor
- Difficulty: beginner
- Subcategory: IDOR
- Tags: idor, api, authorization, bypass
- Original Extracted Source: original extracted web-security-wiki source/api-idor.md
Description:
Exploit an IDOR vulnerability to access unauthorized resources
Prerequisites:
- The target references resources by ID
- An authorization-check flaw exists
Execution Outline:
1. 1. Identify ID parameters
2. 2. Enumerate IDs
3. 3. Batch detection
4. 4. Cross-user access
## API Rate-Limit Bypass
- ID: api-rate-limit
- Difficulty: intermediate
- Subcategory: Rate limiting
- Tags: api, rate-limit, bypass, brute-force
- Original Extracted Source: original extracted web-security-wiki source/api-rate-limit.md
Description:
Bypass API rate limiting to perform brute-force attacks
Prerequisites:
- The target has rate limiting
- The rate-limit implementation is flawed
Execution Outline:
1. 1. Detect rate limiting
2. 2. IP bypass
3. 3. Distributed bypass
4. 4. Other bypass techniques
## Mass-Assignment Vulnerability
- ID: api-mass-assignment
- Difficulty: beginner
- Subcategory: Mass assignment
- Tags: api, mass-assignment, privilege-escalation
- Original Extracted Source: original extracted web-security-wiki source/api-mass-assignment.md
Description:
Exploit a mass-assignment vulnerability to modify sensitive fields
Prerequisites:
- The API accepts JSON input
- Unfiltered fields exist
Execution Outline:
1. 1. Identify input fields
2. 2. Add a sensitive field
3. 3. Update operation
4. 4. Nested objects
## BOLA (Broken Object Level Authorization)
- ID: api-bola
- Difficulty: intermediate
- Subcategory: BOLA
- Tags: api, bola, authorization, idor
- Original Extracted Source: original extracted web-security-wiki source/api-bola.md
Description:
Exploit a BOLA vulnerability to access unauthorized objects
Prerequisites:
- The API uses object IDs
- Authorization-check flaw
Execution Outline:
1. 1. Identify object access
2. 2. Test authorization
3. 3. Lateral access
4. 4. Modify/delete operations
## API Injection Attacks
- ID: api-injection
- Difficulty: intermediate
- Subcategory: API injection
- Tags: api, injection, sqli, nosqli
- Original Extracted Source: original extracted web-security-wiki source/api-injection.md
Description:
Various injection attacks in API endpoints
Prerequisites:
- The API accepts user input
- Input is not properly filtered
Execution Outline:
1. 1. SQL injection
2. 2. NoSQL injection
3. 3. LDAP injection
4. 4. Command injection

