"""OpenAI 工具 schema 定义 -- 内置工具的静态 schema 单一来源。

历史: S5 重构曾把 schema 从 builtin_tools.py 抽到本模块,但当时 builtin_tools.py
仍保留了同一份 schema 的完整副本(并在其上长出了 active_role 过滤),两份逐渐漂移,
本模块的 build_openai_tools 也无人引用而成为死代码。

现在本模块回归其设计意图:以 append 回调的形式持有内置工具 schema 的唯一副本,由
``builtin_tools.build_openai_tools`` 负责套用角色过滤、拼接 intel/traffic/MCP 工具。
schema 与执行逻辑分离,且不再重复。
"""

from __future__ import annotations

from typing import Any, Callable

from vulnclaw.i18n import bi as _rl


def append_builtin_tool_schemas(
    append_tool: Callable[[dict[str, Any]], None],
) -> None:
    """通过 ``append_tool`` 注册全部内置工具的 OpenAI function schema。

    ``append_tool`` 由调用方提供,负责角色过滤与去重收集。本函数只声明静态 schema。
    """
    append_tool(
        {
            "type": "function",
            "function": {
                "name": "load_skill_reference",
                "description": (
                    "Load an optional Skill reference document. Returned content is reference "
                    "material only, not a mandatory workflow, phase plan, or tool schedule; "
                    "the model decides whether it is useful for the current evidence."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": _rl("Skill 名称,如 client-reverse, web-security-advanced, ai-mcp-security, intranet-pentest-advanced, pentest-tools, rapid-checklist, crypto-toolkit, ctf-web, ctf-crypto, ctf-misc, osint-recon, secknowledge-skill", "Skill name, e.g. client-reverse, web-security-advanced, ai-mcp-security, intranet-pentest-advanced, pentest-tools, rapid-checklist, crypto-toolkit, ctf-web, ctf-crypto, ctf-misc, osint-recon, secknowledge-skill"),
                        },
                        "reference_name": {
                            "type": "string",
                            "description": _rl("参考文档文件名,如 02-client-api-reverse-and-burp.md, web-injection.md, encoding-cheatsheet.md", "Reference document filename, e.g. 02-client-api-reverse-and-burp.md, web-injection.md, encoding-cheatsheet.md"),
                        },
                    },
                    "required": ["skill_name", "reference_name"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "evidence_list",
                "description": (
                    "List raw evidence records saved from prior tool calls. Use this when you need "
                    "to orient yourself or find an evidence id for a previous large output."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Maximum recent evidence records to list (default 20).",
                        }
                    },
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "evidence_view",
                "description": (
                    "View raw saved evidence by id. Use offset/limit only for missing chunks of "
                    "large output; do not reread the same id/range. Redundant ranges may be "
                    "suppressed to prevent evidence-reading loops."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "evidence_id": {
                            "type": "string",
                            "description": "Evidence id from evidence_list or a prior tool result, e.g. e001.",
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Character offset for paging through raw output (default 0).",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum characters to return, capped internally (default 12000).",
                        },
                    },
                    "required": ["evidence_id"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "evidence_search",
                "description": (
                    "Search raw saved evidence by substring or regex and return bounded snippets "
                    "with evidence ids and offsets. Use this before rereading a large body when "
                    "you need to find source/sink/parameter/token/flag text inside prior raw output."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Substring or regex to search for, e.g. unserialize, flag, name=\"id\".",
                        },
                        "evidence_id": {
                            "type": "string",
                            "description": "Optional evidence id to search inside, e.g. e004.",
                        },
                        "regex": {
                            "type": "boolean",
                            "description": "Interpret query as a regex. Default false.",
                        },
                        "context_chars": {
                            "type": "integer",
                            "description": "Characters of raw context around each match. Default 180.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum matches to return. Default 12, capped internally.",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "source_extract",
                "description": (
                    "Normalize messy HTML/highlight_file/source evidence into readable text and "
                    "extract high-signal PHP/web surfaces such as forms, endpoints, unserialize, "
                    "magic methods, eval sinks, taint sources and filters. Use it when raw body "
                    "contains highlighted or noisy source code."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "evidence_id": {
                            "type": "string",
                            "description": "Evidence id to normalize, e.g. e004. Prefer this for saved fetch/http outputs.",
                        },
                        "text": {
                            "type": "string",
                            "description": "Inline raw HTML/source text to normalize when no evidence id exists.",
                        },
                    },
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "runtime_diff_probe",
                "description": (
                    "Run a compact local parser/filter differential table. Use when evidence shows "
                    "a regex/string filter before a runtime parser/interpreter and you need to find "
                    "inputs accepted by the parser but missed by the filter. Supports generic regex "
                    "checks and PHP serialize/unserialize checks; this is local verification only."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {
                            "type": "string",
                            "description": "regex or php_serialize. Default regex.",
                        },
                        "filter_regex": {
                            "type": "string",
                            "description": "Observed filter regex, e.g. /[oc]:\\d+:/i.",
                        },
                        "payload": {
                            "type": "string",
                            "description": "Canonical payload to mutate and compare against the filter/parser.",
                        },
                        "candidates": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "payload": {"type": "string"},
                                },
                            },
                            "description": "Optional explicit candidate payloads to test.",
                        },
                        "mutations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": (
                                "Optional mutation names. For php_serialize: signed_lengths, "
                                "leading_zero_lengths, lowercase_type, uppercase_string_type."
                            ),
                        },
                        "class_defs": {
                            "type": "string",
                            "description": (
                                "PHP class definitions for php_serialize mode, without <?php tags. "
                                "Use minimal local definitions needed to validate unserialize behavior."
                            ),
                        },
                        "target_runtime": {
                            "type": "string",
                            "description": (
                                "Optional target runtime/version observed from headers/source, e.g. "
                                "PHP/5.6.40. If omitted, VulnClaw tries to infer it from evidence."
                            ),
                        },
                        "timeout_ms": {
                            "type": "integer",
                            "description": "Local runtime timeout in milliseconds, default 10000.",
                        },
                        "max_output_chars": {
                            "type": "integer",
                            "description": (
                                "Optional command-level output cap before evidence storage; omitted "
                                "or 0 keeps raw output intact, while large active-context observations "
                                "may still be represented by a high-signal preview."
                            ),
                        },
                    },
                    "required": ["filter_regex"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "shell_command",
                "description": (
                    "Run a local shell command when local verification or exact request fidelity is "
                    "useful. Good uses include php -r serialization checks, curl requests with raw "
                    "cookies/headers, rg/Select-String over saved files, and small one-off scripts. "
                    "Set workdir when the command depends on files. Raw stdout/stderr are saved as "
                    "evidence; large active-context observations are bounded high-signal previews."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Shell command to run."},
                        "workdir": {
                            "type": "string",
                            "description": "Working directory. Defaults to the VulnClaw process cwd.",
                        },
                        "timeout_ms": {
                            "type": "integer",
                            "description": "Command timeout in milliseconds, default 10000, capped at 120000.",
                        },
                        "shell": {
                            "type": "string",
                            "description": "Windows: powershell (default), pwsh, or cmd. Other OSes use the default shell.",
                        },
                        "max_output_chars": {
                            "type": "integer",
                            "description": (
                                "Optional command-level output cap before evidence storage; omitted "
                                "or 0 keeps raw output intact, while large active-context observations "
                                "may still be represented by a high-signal preview."
                            ),
                        },
                        "risk_self_assessment": {
                            "type": "string",
                            "enum": ["safe", "review"],
                            "description": (
                                "Your own risk judgement for this command. 'review' requests "
                                "explicit operator approval before it runs (recommended for "
                                "anything touching credentials, host config, or destructive "
                                "operations); 'safe' or omitted leaves the decision to the "
                                "local whitelist. Self-assessment can only escalate to a human — "
                                "it can never make a blocked command run."
                            ),
                        },
                        "assessment_reason": {
                            "type": "string",
                            "maxLength": 300,
                            "description": "Shown to the approver alongside the command.",
                        },
                    },
                    "required": ["command"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "http_probe_batch",
                "description": (
                    "Batch HTTP probe tool for comparing many URL/parameter/header/body variants "
                    "in one call. Use it when repeated fetch/python_execute calls would only differ "
                    "by payload, query params, raw URL encoding, headers, or POST body. It returns "
                    "status/length/hash/title/body signals, the audited request surface, same-body "
                    "groups, and raw response bodies saved as evidence. Large active-context "
                    "observations are bounded high-signal previews."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base_url": {
                            "type": "string",
                            "description": "Optional base URL used to resolve relative request urls.",
                        },
                        "requests": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "method": {
                                        "type": "string",
                                        "description": "GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS; default GET.",
                                    },
                                    "url": {
                                        "type": "string",
                                        "description": "Full or relative URL. Params are encoded via params.",
                                    },
                                    "raw_url": {
                                        "type": "string",
                                        "description": "Full or relative URL sent exactly as supplied; params is ignored.",
                                    },
                                    "params": {
                                        "type": "object",
                                        "description": "Query parameters for url mode.",
                                    },
                                    "headers": {
                                        "type": "object",
                                        "description": (
                                            "Per-request headers. For exact Cookie payloads or values "
                                            "containing semicolons/quotes/braces, prefer headers.Cookie "
                                            "with the already-encoded raw value."
                                        ),
                                    },
                                    "cookies": {
                                        "type": "object",
                                        "description": (
                                            "Simple per-request cookies. Use headers.Cookie instead "
                                            "when cookie serialization/encoding must be exact."
                                        ),
                                    },
                                    "data": {
                                        "description": "Form body or raw body for POST/OPTIONS probes."
                                    },
                                    "json": {"description": "JSON body for POST/OPTIONS probes."},
                                    "label": {"type": "string", "description": "Short label for the variant."},
                                },
                            },
                            "description": "Probe variants, max 30 per call.",
                        },
                        "timeout": {"type": "number", "description": "Per-request timeout seconds, 1-30."},
                        "follow_redirects": {
                            "type": "boolean",
                            "description": "Whether to follow redirects; default true.",
                        },
                        "verify_tls": {
                            "type": "boolean",
                            "description": "Verify TLS certificates; default false for CTF/lab compatibility.",
                        },
                        "max_body_chars": {
                            "type": "integer",
                            "description": "Optional max body chars per response; omitted or 0 returns full bodies.",
                        },
                    },
                    "required": ["requests"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "python_execute",
                "description": (
                    _rl("执行 Python 代码片段。用于:构造复杂 HTTP 请求并解析响应、"
                    "做编码转换和数据处理、批量测试不同 payload、比较响应差异、"
                    "执行数学计算等。代码在受限环境中执行,超时 30 秒。"
                    "预装库:requests, beautifulsoup4, pycryptodome, base64, json, re 等。"
                    "普通 HTTP/HTTPS 请求优先使用 fetch 或 http_probe_batch,避免用 Python 手写请求浪费上下文;"
                    "只有需要复杂解析、生成 payload 或批量逻辑时再使用此工具。", "Execute a Python code snippet. Useful for building complex HTTP requests and parsing responses, encoding conversions and data processing, batch-testing different payloads, comparing response differences, doing math, etc. Code runs in a restricted environment with a 30-second timeout. Preinstalled libraries: requests, beautifulsoup4, pycryptodome, base64, json, re, and others. For ordinary HTTP/HTTPS requests prefer fetch or http_probe_batch to avoid wasting context on hand-written Python requests; use this tool only when you need complex parsing, payload generation, or batch logic.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": _rl("要执行的 Python 代码。支持多行,可 import 标准库和 requests/bs4 等。", "The Python code to execute. Multi-line is supported; you may import the standard library and requests/bs4, etc."),
                        },
                        "purpose": {
                            "type": "string",
                            "description": _rl("简要说明执行目的(用于审计日志),如'构造HTTP请求测试弱比较绕过'", "A brief description of the purpose (for the audit log), e.g. 'build an HTTP request to test loose-comparison bypass'"),
                        },
                        "risk_self_assessment": {
                            "type": "string",
                            "enum": ["safe", "review"],
                            "description": (
                                _rl("你对该段代码风险的自我判断。'review' 会请求操作者人工批准后"
                                "才执行(推荐用于触碰凭据、宿主配置或具破坏性的代码);"
                                "'safe'/省略不改变本工具始终需要审批的默认行为。"
                                "自评只能升级为人工审核,不能使被拦命令放行。", "Your own risk judgement for this code. 'review' requests explicit operator approval before it runs (recommended for anything touching credentials, host config, or destructive code); 'safe' or omitted does not change this tool's default of always requiring approval. Self-assessment can only escalate to human review — it can never make a blocked command run.")
                            ),
                        },
                        "assessment_reason": {
                            "type": "string",
                            "maxLength": 300,
                            "description": _rl("展示给审批者的自评理由。", "The self-assessment reason shown to the approver."),
                        },
                    },
                    "required": ["code"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "crypto_decode",
                "description": (
                    _rl("编码解码与加解密工具。遇到 base64/hex/URL/HTML/Unicode 编码字符串、"
                    "需要计算哈希、解密 AES/DES、解析 JWT 等场景时调用此工具。"
                    "重要:不要自行脑补解码结果,始终使用此工具确保准确性。"
                    "支持操作:base64_encode/decode, base32_encode/decode, base58_encode/decode, "
                    "hex_encode/decode, url_encode/decode, html_encode/decode, unicode_encode/decode, "
                    "rot13_encode/decode, caesar_encode/decode, morse_encode/decode, "
                    "md5_hash, sha1_hash, sha256_hash, sha512_hash, "
                    "aes_encrypt/decrypt, jwt_decode/encode, auto_decode", "Encoding/decoding and encryption/decryption tool. Call it for base64/hex/URL/HTML/Unicode encoded strings, hash computation, AES/DES decryption, JWT parsing, and similar tasks. Important: do not guess decoding results yourself; always use this tool for accuracy. Supported operations: base64_encode/decode, base32_encode/decode, base58_encode/decode, hex_encode/decode, url_encode/decode, html_encode/decode, unicode_encode/decode, rot13_encode/decode, caesar_encode/decode, morse_encode/decode, md5_hash, sha1_hash, sha256_hash, sha512_hash, aes_encrypt/decrypt, jwt_decode/encode, auto_decode")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": _rl("操作名称", "Operation name")},
                        "input": {
                            "type": "string",
                            "description": _rl("待处理的输入字符串(待编码/解码/哈希/加密的文本)", "The input string to process (the text to encode/decode/hash/encrypt)"),
                        },
                        "key": {
                            "type": "string",
                            "description": _rl("加密/解密密钥(AES/DES 需要,16/24/32字节)", "Encryption/decryption key (required for AES/DES, 16/24/32 bytes)"),
                        },
                        "iv": {"type": "string", "description": _rl("AES 初始化向量(16字节,可选)", "AES initialization vector (16 bytes, optional)")},
                        "shift": {
                            "type": "integer",
                            "description": _rl("Caesar 密码位移量(默认3,解码时不提供则暴力所有位移)", "Caesar cipher shift amount (default 3; if omitted when decoding, brute-forces all shifts)"),
                        },
                        "secret": {"type": "string", "description": _rl("JWT 签名密钥", "JWT signing key")},
                    },
                    "required": ["operation", "input"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "nmap_scan",
                "description": (
                    _rl("nmap 网络端口扫描工具。适合在端口、服务版本或网络暴露面会影响下一步判断时使用。\n"
                    "用法示例:\n"
                    "  扫描常见端口: scan_type=top_ports, target=1.2.3.4\n"
                    "  SYN扫描: scan_type=syn, target=1.2.3.4(需要管理员权限)\n"
                    "  服务版本检测: scan_type=service, target=1.2.3.4\n"
                    "  漏洞扫描: scan_type=vuln, target=1.2.3.4\n"
                    "  全量扫描: scan_type=full, target=1.2.3.4\n"
                    "如果只需验证一个具体 HTTP/Web 行为,可以选择其他更轻量工具。", "nmap network port-scanning tool. Use it when ports, service versions, or network exposure will affect the next decision.\nUsage examples:\n  Scan common ports: scan_type=top_ports, target=1.2.3.4\n  SYN scan: scan_type=syn, target=1.2.3.4 (requires administrator privileges)\n  Service version detection: scan_type=service, target=1.2.3.4\n  Vulnerability scan: scan_type=vuln, target=1.2.3.4\n  Full scan: scan_type=full, target=1.2.3.4\nIf you only need to verify one specific HTTP/Web behavior, choose a lighter-weight tool instead.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": _rl("目标 IP 地址或域名(必填),如 192.168.1.1 或 scanme.nmap.org", "Target IP address or domain (required), e.g. 192.168.1.1 or scanme.nmap.org"),
                        },
                        "scan_type": {
                            "type": "string",
                            "description": _rl("扫描类型:top_ports/syn/tcp/service/os/vuln/full", "Scan type: top_ports/syn/tcp/service/os/vuln/full"),
                        },
                        "ports": {
                            "type": "string",
                            "description": _rl("指定端口或范围(可选),如 80,443,8080 或 1-1000", "Specific ports or range (optional), e.g. 80,443,8080 or 1-1000"),
                        },
                        "timing": {
                            "type": "integer",
                            "description": _rl("扫描速度模板 0-5(默认4),数字越大越快但越容易被检测", "Scan timing template 0-5 (default 4); higher is faster but more easily detected"),
                        },
                        "profile": {
                            "type": "string",
                            "description": _rl("可选网络扫描画像:adaptive/fast/thorough/stealth。画像会联动调整端口、速度、服务探测与安全脚本。", "Optional network-scan profile: adaptive/fast/thorough/stealth. The profile jointly adjusts ports, timing, service probing, and safe scripts."),
                        },
                    },
                    "required": ["target"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "brute_force_login",
                "description": (
                    _rl("对登录表单进行密码爆破。自动管理 Session Cookie、"
                    "自动提取和更新 CSRF Token、判断登录成功/失败。"
                    "单次调用内完成所有密码尝试,返回每个密码的结果。", "Brute-force passwords against a login form. Automatically manages the session cookie, extracts and refreshes the CSRF token, and judges login success/failure. Completes all password attempts in a single call and returns the result for each password.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": _rl("登录页面 URL", "Login page URL"),
                        },
                        "username_field": {
                            "type": "string",
                            "description": _rl("用户名字段名,如 'username'", "Username field name, e.g. 'username'"),
                        },
                        "password_field": {
                            "type": "string",
                            "description": _rl("密码字段名,如 'password'", "Password field name, e.g. 'password'"),
                        },
                        "csrf_field": {
                            "type": "string",
                            "description": _rl("CSRF token 字段名,如 'user_token'", "CSRF token field name, e.g. 'user_token'"),
                        },
                        "username": {
                            "type": "string",
                            "description": _rl("要爆破的用户名", "The username to brute-force"),
                        },
                        "passwords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": _rl("要尝试的密码列表(最多 20 个)", "List of passwords to try (up to 20)"),
                        },
                        "success_keyword": {
                            "type": "string",
                            "description": _rl("登录成功后页面出现的特征词,如 'Welcome'、'Dashboard'", "Keyword that appears on the page after a successful login, e.g. 'Welcome', 'Dashboard'"),
                        },
                        "failure_keyword": {
                            "type": "string",
                            "description": _rl("登录失败后页面出现的特征词,如 'Login failed'", "Keyword that appears on the page after a failed login, e.g. 'Login failed'"),
                        },
                        "submit_action": {
                            "type": "string",
                            "description": _rl("表单提交的目标 URL(可选,不指定则从表单 action 属性提取)", "Form submission target URL (optional; if omitted, extracted from the form's action attribute)"),
                        },
                        "extra_data": {
                            "type": "object",
                            "description": _rl("额外表单字段,如 {\"Login\": \"Login\"}", "Extra form fields, e.g. {\"Login\": \"Login\"}"),
                        },
                    },
                    "required": ["url", "password_field", "passwords"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "space_search",
                "description": (
                    _rl("空间测绘资产搜索(FOFA/Hunter/Quake/Shodan/ZoomEye/0.zone 零零信安)。"
                    "可在需要被动发现目标资产、IP、端口、子域、标题或组件指纹时使用,不直接接触目标。"
                    "给 domain 自动按各引擎语法构造 domain 查询;也可传完整 query 语法。"
                    "engine=all 时并发查询所有已配置 key 的引擎。", "Cyberspace-mapping asset search (FOFA/Hunter/Quake/Shodan/ZoomEye/0.zone). Use it to passively discover target assets, IPs, ports, subdomains, titles, or component fingerprints without touching the target directly. Given a domain it builds the per-engine domain query automatically; you can also pass full query syntax. With engine=all it queries every engine that has a configured key concurrently.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "engine": {
                            "type": "string",
                            "description": _rl("fofa/hunter/quake/shodan/zoomeye/zerozone/all,默认 fofa", "fofa/hunter/quake/shodan/zoomeye/zerozone/all, default fofa"),
                        },
                        "query": {
                            "type": "string",
                            "description": _rl("引擎原生查询语法,如 'domain=\"x.com\"'、'app=\"Struts2\"'(可选)", "Engine-native query syntax, e.g. 'domain=\"x.com\"', 'app=\"Struts2\"' (optional)"),
                        },
                        "domain": {
                            "type": "string",
                            "description": _rl("目标主域名,自动构造各引擎 domain 查询(query 未给时使用)", "Target root domain; builds the per-engine domain query automatically (used when query is not given)"),
                        },
                        "size": {"type": "integer", "description": _rl("返回条数,默认 100", "Number of results to return, default 100")},
                    },
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "subdomain_enum",
                "description": (
                    _rl("子域名枚举。先用已配置的空间测绘引擎被动聚合,再用内置小字典做 DNS 解析爆破,"
                    "返回去重后的存活子域名列表;是否需要枚举由模型根据当前任务判断。", "Subdomain enumeration. First aggregates passively via the configured cyberspace-mapping engines, then brute-forces DNS resolution with a small built-in wordlist, returning a deduplicated list of live subdomains; the model decides whether enumeration is needed for the current task.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string", "description": _rl("主域名,如 nju.edu.cn", "Root domain, e.g. nju.edu.cn")},
                        "brute": {
                            "type": "boolean",
                            "description": _rl("是否启用内置字典 DNS 爆破(默认 true)", "Whether to enable built-in wordlist DNS brute-forcing (default true)"),
                        },
                    },
                    "required": ["domain"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "js_recon",
                "description": (
                    _rl("JS 信息收集(参考 URLFinder)。抓取目标页面及其引用的全部 .js 文件,"
                    "提取 API 接口/路径、关联域名、绝对 URL,以及疑似硬编码密钥(AK/SK、token、JWT、私钥等)。"
                    "默认 auto_probe=true:自动对收集到的同源接口逐个做未授权访问探测(仅安全 GET,跳过破坏性接口)。"
                    "适合在页面脚本可能包含端点、路径或硬编码线索时按需调用。", "JS reconnaissance (inspired by URLFinder). Fetches the target page and every .js file it references, extracting API endpoints/paths, related domains, absolute URLs, and suspected hard-coded secrets (AK/SK, tokens, JWTs, private keys, etc.). Defaults to auto_probe=true: automatically runs unauthorized-access probes against each same-origin endpoint collected (safe GET only, skipping destructive endpoints). Use it when page scripts may contain endpoints, paths, or hard-coded clues.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": _rl("目标页面 URL", "Target page URL")},
                        "max_js": {
                            "type": "integer",
                            "description": _rl("最多抓取的 JS 文件数(默认 30)", "Maximum number of JS files to fetch (default 30)"),
                        },
                        "auto_probe": {
                            "type": "boolean",
                            "description": _rl("是否自动对收集到的接口做未授权探测(默认 true)", "Whether to automatically run unauthorized-access probes against the collected endpoints (default true)"),
                        },
                        "auth_header": {
                            "type": "string",
                            "description": _rl("可选鉴权头做差分对比,如 'Authorization: Bearer xxx',验证无 token 是否也能拿到数据", "Optional auth header for a differential comparison, e.g. 'Authorization: Bearer xxx', to verify whether the same data is returned without a token"),
                        },
                    },
                    "required": ["url"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "unauth_test",
                "description": (
                    _rl("未授权访问探测。对一批接口(通常来自 js_recon 收集的端点)逐个无凭据请求,"
                    "按状态码/响应体/内容类型判定:⚠疑似未授权(返回数据) / ✓已鉴权拦截 / ↪跳转登录 / -不存在。"
                    "提供 auth_header 时做有/无 token 差分对比,无 token 也能拿到同样数据则判定 🔴未授权确认。"
                    "严守读写分离:仅发安全 GET,自动跳过 delete/update/sms 等破坏性接口,不批量遍历 ID。", "Unauthorized-access probe. Sends credential-less requests to a batch of endpoints (usually collected by js_recon), judging each by status code / response body / content type: ⚠ likely unauthorized (returns data) / ✓ auth-blocked / ↪ redirect to login / - not found. When auth_header is provided it runs a with-/without-token differential; if the same data is returned without a token it flags 🔴 confirmed unauthorized. Strict read/write separation: only safe GET requests, automatically skipping destructive endpoints such as delete/update/sms, and never brute-iterating IDs.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base_url": {"type": "string", "description": _rl("目标基础 URL(确定同源范围)", "Target base URL (defines the same-origin scope)")},
                        "endpoints": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": _rl("待测接口路径/URL 列表(来自 js_recon 的接口/路径)", "List of endpoint paths/URLs to test (the endpoints/paths from js_recon)"),
                        },
                        "auth_header": {
                            "type": "string",
                            "description": _rl("可选鉴权头做差分,如 'Authorization: Bearer xxx' 或 'Cookie: session=...'", "Optional auth header for a differential, e.g. 'Authorization: Bearer xxx' or 'Cookie: session=...'"),
                        },
                        "max_endpoints": {
                            "type": "integer",
                            "description": _rl("最多探测的接口数(默认 60)", "Maximum number of endpoints to probe (default 60)"),
                        },
                    },
                    "required": ["base_url", "endpoints"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "dir_enum",
                "description": (
                    _rl("目录/文件枚举(参考 dirsearch)。并发字典爆破,自带 404 基线与全局伪装响应识别"
                    "(随机路径返回 200 即判定伪装并停止)、状态码与响应长度过滤。"
                    "仅做安全的 GET 探测,不碰 delete/update 等破坏性路径。", "Directory/file enumeration (inspired by dirsearch). Concurrent wordlist brute-forcing with a built-in 404 baseline and global soft-404 (masking) detection (if a random path returns 200 it declares masking and stops), plus status-code and response-length filtering. Safe GET probes only; never touches destructive paths such as delete/update.")
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": _rl("目标基础 URL,如 https://x.com/", "Target base URL, e.g. https://x.com/")},
                        "extensions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": _rl("扩展名展开,如 ['php','jsp','bak','zip'](可选)", "Extension expansion, e.g. ['php','jsp','bak','zip'] (optional)"),
                        },
                        "wordlist": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": _rl("追加的自定义路径(基于命名规律的启发式字典,可选)", "Additional custom paths (a heuristic wordlist based on naming patterns, optional)"),
                        },
                    },
                    "required": ["url"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "vault_archive",
                "description": (
                    "Archive an older range of conversation messages into compact vault storage: "
                    "tier 1 (archive) replaces the range with a short pointer, tier 2 (distill) "
                    "with a structured summary, tier 3 (digest) folds it into the global digest. "
                    "The original text is persisted to disk and stays searchable/restorable. "
                    "Use the ‹v#NNNNN› refs visible in the transcript to specify start/end. "
                    "The recent protected tail and the last user message are excluded unless "
                    "force=true."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "string",
                            "description": "Start vault ref, e.g. ‹v#00001›.",
                        },
                        "end": {
                            "type": "string",
                            "description": "End vault ref, e.g. ‹v#00042›.",
                        },
                        "tier": {
                            "type": "integer",
                            "description": "1=archive (pointer), 2=distill (summary), 3=digest (fold into global digest). Default 2.",
                        },
                        "topic": {
                            "type": "string",
                            "description": "Short label describing the archived range, e.g. 'dir_enum on /admin'.",
                        },
                        "summary": {
                            "type": "string",
                            "description": "Optional distilled summary text for tier 2/3.",
                        },
                        "force": {
                            "type": "boolean",
                            "description": "Allow archiving into the protected recent tail (default false).",
                        },
                    },
                    "required": ["start", "end"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "vault_restore",
                "description": (
                    "Mark one or more vault blocks as restored so their messages become "
                    "archivable again. The original text is already persisted; this only "
                    "releases the block's hold on the range."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "string",
                            "description": "Start vault ref of the block to restore, e.g. ‹v#00010›.",
                        },
                        "end": {
                            "type": "string",
                            "description": "End vault ref of the block to restore, e.g. ‹v#00020›.",
                        },
                    },
                    "required": ["start", "end"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "vault_search",
                "description": (
                    "Search archived vault blocks (summaries/topics) for a keyword without "
                    "restoring them into context. Returns bounded hit records with block ids "
                    "and refs so you can decide whether to restore or cite the evidence."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Keyword or phrase to search for in archived summaries.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum hits to return (default 8).",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "vault_status",
                "description": (
                    "Show vault stats: next ref id, active/restored blocks, archived message "
                    "count and approximate characters saved."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        }
    )

    append_tool(
        {
            "type": "function",
            "function": {
                "name": "memory_search",
                "description": (
                    "Search conversation turns moved out of the short-term context into local "
                    "cold storage. Call this only when an older decision, tool result, or clue is "
                    "needed for the current subtask; archived history is not included automatically."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Keyword or phrase expected in older conversation history.",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum archived turns to return (default 5, maximum 20).",
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    )

