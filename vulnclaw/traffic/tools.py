"""Agent-facing traffic tools (in-process builtins).

``traffic_list`` / ``traffic_view`` / ``traffic_repeat`` / ``traffic_sitemap``
read and write the in-sandbox store directly — no MCP round-trip. They return
agent-readable strings (like ``python_execute``), with ``request_id`` surfaced
so the model can chain list → view → repeat and cite a capture in a finding.
"""

from __future__ import annotations

from typing import Any

from vulnclaw.i18n import bi as _rl
from vulnclaw.traffic.replay import ReplayError, replay_request
from vulnclaw.traffic.store import TrafficStore

TRAFFIC_TOOL_NAMES = frozenset(
    {"traffic_list", "traffic_view", "traffic_repeat", "traffic_sitemap"}
)

_MAX_BLOB_CHARS = 4000


def traffic_tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "traffic_list",
                "description": _rl(
                    (
                        "列出本次运行已抓取的 HTTP 请求/响应（来自代理、浏览器或手动重放）。"
                        "用于查看流量索引、按方法/主机/状态码/来源过滤，"
                        "并获取 request_id 以便 traffic_view / traffic_repeat 引用。"
                    ),
                    (
                        "List the HTTP requests/responses captured during this run (from the proxy, "
                        "browser, or manual replay). Use it to view the traffic index, filter by "
                        "method/host/status/source, and obtain a request_id for traffic_view / traffic_repeat."
                    ),
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "method": {"type": "string", "description": _rl("按 HTTP 方法过滤，如 GET/POST", "Filter by HTTP method, e.g. GET/POST")},
                        "host": {"type": "string", "description": _rl("按主机过滤，如 app.test", "Filter by host, e.g. app.test")},
                        "status": {"type": "integer", "description": _rl("按响应状态码过滤，如 200", "Filter by response status code, e.g. 200")},
                        "source": {
                            "type": "string",
                            "description": _rl("按来源过滤：proxy/browser/manual-replay", "Filter by source: proxy/browser/manual-replay"),
                        },
                        "limit": {"type": "integer", "description": _rl("返回条数上限（默认 50）", "Maximum number of entries to return (default 50)")},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "traffic_view",
                "description": _rl(
                    (
                        "查看某个已抓取请求的原始请求与响应报文（通过 request_id 定位）。"
                        "用于确认漏洞证据、提取响应细节，并作为发现的 http_capture 证据。"
                    ),
                    (
                        "View the raw request and response of a captured request (located by request_id). "
                        "Use it to confirm vulnerability evidence, extract response details, and cite it as "
                        "http_capture evidence for a finding."
                    ),
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request_id": {"type": "string", "description": _rl("traffic_list 返回的 request_id", "request_id returned by traffic_list")}
                    },
                    "required": ["request_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "traffic_repeat",
                "description": _rl(
                    (
                        "重放一个已抓取的请求，可覆盖 method/url/headers/body，用于验证漏洞、"
                        "修改参数测试或对比响应差异。重放结果会以 source=manual-replay 记录到流量存储，"
                        "并返回新的 request_id。"
                    ),
                    (
                        "Replay a captured request, optionally overriding method/url/headers/body, to verify a "
                        "vulnerability, test with modified parameters, or compare response differences. The replay "
                        "is recorded to the traffic store with source=manual-replay and returns a new request_id."
                    ),
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request_id": {"type": "string", "description": _rl("要重放的原始 request_id", "The original request_id to replay")},
                        "method": {"type": "string", "description": _rl("覆盖 HTTP 方法（可选）", "Override the HTTP method (optional)")},
                        "url": {"type": "string", "description": _rl("覆盖请求 URL（可选）", "Override the request URL (optional)")},
                        "headers": {
                            "type": "object",
                            "description": _rl("覆盖/新增请求头（值为 null 表示删除该头）", "Override/add request headers (a null value removes that header)"),
                        },
                        "body": {"type": "string", "description": _rl("覆盖请求体（可选）", "Override the request body (optional)")},
                    },
                    "required": ["request_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "traffic_sitemap",
                "description": _rl(
                    (
                        "查看本次运行抓取到的站点地图：按主机聚合的路径、方法与命中次数。"
                        "用于快速了解目标攻击面与已覆盖的端点。"
                    ),
                    (
                        "View the sitemap captured during this run: paths, methods and hit counts aggregated by "
                        "host. Use it to quickly understand the target attack surface and the endpoints covered."
                    ),
                ),
                "parameters": {"type": "object", "properties": {}},
            },
        },
    ]


def traffic_list(
    store: TrafficStore,
    *,
    method: str | None = None,
    host: str | None = None,
    status: int | None = None,
    source: str | None = None,
    limit: int = 50,
) -> str:
    rows = store.entries()
    if method:
        rows = [r for r in rows if str(r.get("method", "")).upper() == method.upper()]
    if host:
        rows = [r for r in rows if host.lower() in str(r.get("host", "")).lower()]
    if status is not None:
        rows = [r for r in rows if int(r.get("status", 0)) == int(status)]
    if source:
        rows = [r for r in rows if str(r.get("source", "")) == source]

    total = len(rows)
    if limit and limit > 0:
        rows = rows[-limit:]
    if not rows:
        return _rl("[traffic] 没有匹配的抓包记录。", "[traffic] No matching captures.")

    lines = [_rl(f"[traffic] 共 {total} 条抓包记录（显示 {len(rows)} 条）：", f"[traffic] {total} capture(s) total (showing {len(rows)}):")]
    for r in rows:
        lines.append(
            f"  {r.get('request_id')}  {r.get('method')} {r.get('url')} "
            f"-> {r.get('status')} [{r.get('source')}] {r.get('content_length')}B"
        )
    return "\n".join(lines)


def _truncate(text: str) -> str:
    if len(text) <= _MAX_BLOB_CHARS:
        return text
    return text[:_MAX_BLOB_CHARS] + f"\n... [truncated {len(text) - _MAX_BLOB_CHARS} chars]"


def traffic_view(store: TrafficStore, request_id: str) -> str:
    view = store.view(request_id)
    if view is None:
        return _rl(f"[traffic] 未找到 request_id: {request_id}", f"[traffic] request_id not found: {request_id}")
    parts = [
        f"[traffic] {request_id}  {view.get('method')} {view.get('url')} "
        f"-> {view.get('status')} [{view.get('source')}]",
        "── Request ──",
        _truncate(view.get("request_text", "")) or _rl("(空)", "(empty)"),
    ]
    if view.get("response_text"):
        parts += ["── Response ──", _truncate(view["response_text"])]
    return "\n".join(parts)


def traffic_repeat(
    store: TrafficStore,
    request_id: str,
    overrides: dict[str, Any] | None = None,
    *,
    transport: Any | None = None,
) -> str:
    try:
        record = replay_request(store, request_id, overrides, transport=transport)
    except ReplayError as exc:
        return _rl(f"[traffic] 重放失败: {exc}", f"[traffic] Replay failed: {exc}")
    except Exception as exc:  # network / transport errors
        return _rl(f"[traffic] 重放请求出错: {exc}", f"[traffic] Error replaying request: {exc}")
    return (
        _rl(
            f"[traffic] 已重放 {request_id} -> 新 request_id={record.request_id} "
            f"({record.method} {record.url} -> {record.status}, source=manual-replay)",
            f"[traffic] Replayed {request_id} -> new request_id={record.request_id} "
            f"({record.method} {record.url} -> {record.status}, source=manual-replay)",
        )
    )


def traffic_sitemap(store: TrafficStore) -> str:
    sitemap = store.sitemap()
    if not sitemap:
        return _rl("[traffic] 站点地图为空（尚无抓包）。", "[traffic] Sitemap is empty (no captures yet).")
    lines = [_rl("[traffic] 站点地图：", "[traffic] Sitemap:")]
    for host, paths in sitemap.items():
        lines.append(f"  {host}")
        for leaf in paths:
            methods = ",".join(leaf["methods"])
            lines.append(f"    [{methods}] {leaf['path']} (x{leaf['count']})")
    return "\n".join(lines)


def dispatch_traffic_tool(
    store: TrafficStore, tool_name: str, args: dict[str, Any]
) -> str:
    """Route a traffic tool call to its handler and return an agent string."""
    if tool_name == "traffic_list":
        status = args.get("status")
        return traffic_list(
            store,
            method=args.get("method"),
            host=args.get("host"),
            status=int(status) if status not in (None, "") else None,
            source=args.get("source"),
            limit=int(args.get("limit", 50) or 50),
        )
    if tool_name == "traffic_view":
        return traffic_view(store, str(args.get("request_id", "")))
    if tool_name == "traffic_repeat":
        overrides: dict[str, Any] = {}
        for key in ("method", "url", "headers", "body"):
            if key in args and args[key] is not None:
                overrides[key] = args[key]
        return traffic_repeat(store, str(args.get("request_id", "")), overrides)
    if tool_name == "traffic_sitemap":
        return traffic_sitemap(store)
    return _rl(f"[traffic] 未知工具: {tool_name}", f"[traffic] Unknown tool: {tool_name}")
