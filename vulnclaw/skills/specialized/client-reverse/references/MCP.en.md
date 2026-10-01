# MCP Capabilities Master Document

## 1. Document Purpose

This document collects the MCP capabilities I can call directly in the current session; the goal is not merely a "tool list" but a reference draft suited to writing `skills` later.
It focuses on the following:

- The positioning of each MCP server/namespace
- How each method is called
- The meaning of the main parameters
- Roughly what the returned result will contain
- Typical use scenarios
- Common workflows when combined with other MCPs

This document targets Codex / Agent-style tool orchestration by default, not a general SDK doc. It therefore emphasizes "when to use it" and "how to describe the calling strategy when writing a skill."

---

## 2. General calling conventions

### 2.1 Tool naming format

Most MCP tool names in the current environment follow this format:

```text
mcp__<server_name>__<tool_name>
```

For example:

- `mcp__adb_mcp__list_devices`
- `mcp__chrome_devtools__navigate_page`
- `mcp__ida_pro_mcp__decompile`

A few functions related to MCP resource access do not carry the `mcp__` prefix, but they are essentially MCP-ecosystem capabilities too:

- `list_mcp_resources`
- `list_mcp_resource_templates`
- `read_mcp_resource`

### 2.2 Call parameter format

All MCP tools use JSON-style parameter objects. Typical format:

```json
{
  "device_id": "emulator-5554",
  "lines": 200
}
```

Caveats:

- Pass only the fields you need; don't stuff in empty arrays or `null` pointlessly
- `optional` parameters can generally be omitted
- Some tools require absolute paths, especially for screenshots, saving source, pulling files, and screen-recording output paths
- Some tools use pagination parameters such as `offset`, `count`, `pageIdx`, `pageSize`

### 2.3 Points to describe when writing a skill

If you want to turn these capabilities into skills, each skill should state clearly:

1. Trigger condition
2. The preferred MCP
3. The ordering between tools
4. Which parameters must be filled in
5. When to switch to another MCP
6. What to do next if the output is empty or fails

### 2.4 MCP selection quick reference

| Task type | Preferred MCP |
| --- | --- |
| Android device management, APK install, tap/swipe, file pull | `adb_mcp` |
| Android visual control, UI-tree location, wireless ADB, live screen | `scrcpy_vision` |
| Android HTTP/HTTPS traffic capture, Charles session analysis | `charles` |
| Burp history, Repeater, Collaborator, Intruder | `burp` |
| Web automation, screenshots, forms, network requests, console | `chrome_devtools` |
| JS breakpoints, source search, XHR initiation chain, function tracing | `js_reverse` |
| Official documentation retrieval, code-example lookup | `context7` |
| General web fetching / pulling page content | `fetch` |
| Ultra-fast local file search | `everything_search` |
| Android dynamic injection, Frida attach/spawn | `frida_mcp` |
| Binary static analysis, IDA batch renaming/decompilation/type-fixing | `ida_pro_mcp` |
| APK decompilation, Manifest, class/method/xref queries | `jadx` |
| Memory graph, long-term structured memory | `memory` |
| Step-by-step thinking on complex problems | `sequential_thinking` |

### 2.5 Common combined workflows

#### Android app analysis

- Static: `jadx`
- Dynamic: `frida_mcp`
- Traffic capture: `charles`
- Device control: `adb_mcp`
- Visualization / UI automation: `scrcpy_vision`

#### Web front-end reversing

- Page operations: `chrome_devtools`
- JS breakpoints and source search: `js_reverse`
- HTTP replay and security testing: `burp`

#### Native / APK .so reversing

- IDA static analysis: `ida_pro_mcp`
- Runtime hook: `frida_mcp`
- Device-side assistance: `adb_mcp` / `scrcpy_vision`

---

## 3. MCP resource-class general interfaces

These three kinds of functions are not concrete business servers but general capabilities for "accessing resources exposed by MCP servers."

### 3.1 `list_mcp_resources`

- Purpose: list the resources exposed by a specific MCP server or all servers
- Typical use: find directly readable files, context, database schemas, and config fragments
- Parameters:
  - `server`: optional, specifies the server name
  - `cursor`: optional, pagination cursor
- Skill-friendly description: enumerate resources first, then decide whether to call `read_mcp_resource`

Example:

```json
{
  "server": "some_server"
}
```

### 3.2 `list_mcp_resource_templates`

- Purpose: list parameterized resource templates
- Typical use: discover "parameterized read" resources, e.g. resources queried by table name, primary key, or path
- Parameters:
  - `server`
  - `cursor`
- Skill-friendly description: when a resource is a "template URI" rather than a fixed URI, query this first

### 3.3 `read_mcp_resource`

- Purpose: read the content of a specific resource
- Parameters:
  - `server`: server name
  - `uri`: resource URI
- Suitable scenarios:
  - Read config
  - Read schema
  - Read service context
  - Read shared state

Example:

```json
{
  "server": "some_server",
  "uri": "resource://example/path"
}
```

---

## 4. `adb_mcp`: Android device control and file interaction

### 4.1 Positioning

`adb_mcp` is the most basic Android device-interaction layer, suited for:

- Device listing and state confirmation
- Install/uninstall APKs
- Screenshots, screen recording
- Input text, tap, swipe, send key events
- Pull/push files
- Read logcat, battery, memory, storage info

If your skill needs to "control the device itself," consider it first.

### 4.2 Common workflow

1. `list_devices` to confirm the device
2. `get_device_info` / `get_battery_info` to assess the environment
3. `install_app` or `list_packages`
4. `send_tap` / `send_swipe` / `send_text` to drive interaction
5. `take_screenshot` / `record_screen` to keep evidence
6. `get_logcat` for troubleshooting

### 4.3 Method list

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__adb_mcp__list_devices` | none | List connected Android devices | Task entry point; first confirm the device is online |
| `mcp__adb_mcp__get_device_info` | `device_id?` | Read detailed device info | See model, OS version, serial |
| `mcp__adb_mcp__get_battery_info` | `device_id?` | Read battery status | Confirm charge before long tests |
| `mcp__adb_mcp__get_memory_info` | `device_id?` | Read memory info | Performance/stability troubleshooting |
| `mcp__adb_mcp__get_storage_info` | `device_id?` | Read storage info | Check whether there is enough space to install/record |
| `mcp__adb_mcp__clear_logcat` | `device_id?` | Clear logcat | Do a clean log capture |
| `mcp__adb_mcp__get_logcat` | `device_id?`, `filter_tag?`, `lines?` | Read logs | Crash, network, SSL, debug troubleshooting |
| `mcp__adb_mcp__install_app` | `apk_path`, `device_id?` | Install an APK | Deploy the test build |
| `mcp__adb_mcp__uninstall_app` | `package_name`, `device_id?` | Uninstall an app | Clean up the environment |
| `mcp__adb_mcp__list_packages` | `device_id?`, `system_apps?` | List installed package names | Find the target package name |
| `mcp__adb_mcp__list_files` | `remote_path`, `device_id?` | View device directory | Find caches, configs, exported files |
| `mcp__adb_mcp__pull_file` | `remote_path`, `local_path`, `device_id?` | Pull a file from the device to local | Export databases, logs, caches |
| `mcp__adb_mcp__push_file` | `local_path`, `remote_path`, `device_id?` | Push a file to the device | Push certificates, scripts, patches |
| `mcp__adb_mcp__send_keyevent` | `keycode`, `device_id?` | Send a key event | Back, Home, Menu keys |
| `mcp__adb_mcp__send_tap` | `x`, `y`, `device_id?` | Tap a coordinate | Automated operations |
| `mcp__adb_mcp__send_swipe` | `x1`,`y1`,`x2`,`y2`,`duration?`,`device_id?` | Swipe | Scroll lists, unlock, switch pages |
| `mcp__adb_mcp__send_text` | `text`, `device_id?` | Input text | Search, login, form input |
| `mcp__adb_mcp__take_screenshot` | `save_path`, `device_id?` | Screenshot to local | Evidence retention, UI-state confirmation |
| `mcp__adb_mcp__record_screen` | `duration?`, `save_path?`, `device_id?` | Record the screen | Capture evidence of a reproduced flow |

### 4.4 Typical call examples

List devices:

```json
{}
```

Screenshot:

```json
{
  "device_id": "emulator-5554",
  "save_path": "C:\\Users\\28484\\Desktop\\screen.png"
}
```

Read the most recent 200 log lines:

```json
{
  "device_id": "emulator-5554",
  "lines": 200
}
```

### 4.5 Caveats when writing a skill

- Almost any Android task should run `list_devices` once first
- `take_screenshot` explicitly requires a local absolute path
- For `get_logcat` in complex scenarios, run `clear_logcat` first
- `send_tap` / `send_swipe` rely entirely on coordinates; they suit fixed layouts, not highly dynamic ones
- `push_file` and `pull_file` are high-frequency tools for certificate installation, log export, and evidence retention

---

## 5. `charles`: Charles traffic capture and session analysis

### 5.1 Positioning

`charles` reads and analyzes traffic already captured by Charles Proxy; the focus is not "directly controlling the Android proxy" but rather:

- Check whether Charles is online and whether an active capture session already exists
- Start or take over a live capture and obtain the `capture_id`
- Structured filtering of live traffic or a saved recording
- Drill into a single request to view headers, status code, and request/response body previews
- Analyze traffic grouped by host, path, status, and resource class
- End the capture and persist a snapshot for later review

### 5.2 Suitable skill types

- Android API reversing
- HTTPS traffic capture
- App API behavior analysis
- Before/after comparison of parameter signing
- Find tokens, sessions, encrypted fields
- Session recording, filtering, and evidence retention

### 5.3 Method list

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__charles__charles_status` | none | Check Charles connectivity and live-capture status | Confirm the environment is ready |
| `mcp__charles__reset_environment` | none | Reset the Charles environment and restore saved config | Run a clean experiment |
| `mcp__charles__start_live_capture` | `adopt_existing?`,`include_existing?`,`reset_session?` | Start or take over a live capture | Obtain the `capture_id` for later analysis |
| `mcp__charles__query_live_capture_entries` | `capture_id`,`cursor?`,`preset?`,`host_contains?`,`path_contains?`,`method_in?`,`status_in?`,`request_body_contains?`,`response_body_contains?`,`max_items?` | Structured filtering of live traffic | Recommended real-time retrieval entry |
| `mcp__charles__peek_live_capture` | `capture_id`,`cursor?`,`limit?` | Preview new entries in the current live capture | Lightweight view of recent requests |
| `mcp__charles__read_live_capture` | `capture_id`,`cursor?`,`limit?` | Incrementally read and advance the live cursor | Use when you need to stream new traffic |
| `mcp__charles__get_traffic_entry_detail` | `source`,`entry_id`,`capture_id?`,`recording_path?`,`include_full_body?`,`max_body_chars?` | Drill into a single traffic entry | View headers, body preview, request/response details |
| `mcp__charles__group_capture_analysis` | `source`,`capture_id?`,`recording_path?`,`group_by`,`preset?`,`host_contains?`,`path_contains?`,`status_in?` | Group by host/path/status/resource class | Quickly find hot endpoints |
| `mcp__charles__get_capture_analysis_stats` | `source`,`capture_id?`,`recording_path?`,`preset?` | Return coarse-grained statistics | See the overall capture distribution |
| `mcp__charles__stop_live_capture` | `capture_id`,`persist?` | Stop the live capture, optionally persisting it | End the experiment and save a snapshot |
| `mcp__charles__list_recordings` | none | List saved recording files | Pick a historical traffic capture |
| `mcp__charles__list_sessions` | none | List historical sessions (compatibility) | Backward compatibility for old naming |
| `mcp__charles__get_recording_snapshot` | `path?` | Read snapshot metadata of a saved recording | Inspect a recording offline |
| `mcp__charles__analyze_recorded_traffic` | `recording_path?`,`preset?`,`host_contains?`,`path_contains?`,`method_in?`,`status_in?`,`request_body_contains?`,`response_body_contains?`,`max_items?` | Analyze a saved recording | Offline review and retrospective |
| `mcp__charles__query_recorded_traffic` | `host_contains?`,`http_method?`,`keyword_regex?`,`keep_request?`,`keep_response?` | Query the most recently saved recording | Quickly filter historical traffic |
| `mcp__charles__proxy_by_time` | `record_seconds` | Capture for a fixed duration or read the latest historical capture | Quick time-window analysis |
| `mcp__charles__filter_func` | `capture_seconds`,`host_contains?`,`http_method?`,`keyword_regex?`,`keep_request?`,`keep_response?` | Filter traffic by time window and conditions | Quickly narrow the scope |
| `mcp__charles__throttling` | `preset` | Set a Charles weak-network / throttling preset | Weak-network reproduction and behavior verification |

### 5.4 Recommended workflow

1. `charles_status`  
2. Confirm that Charles is listening, the Android proxy points to the capture machine, and the Charles certificate is installed when HTTPS is needed
3. `reset_environment` (optional, for a clean experiment)
4. `start_live_capture`  
5. Operate the app
6. `query_live_capture_entries`  
7. `get_traffic_entry_detail`  
8. `group_capture_analysis` / `get_capture_analysis_stats`  
9. `stop_live_capture`, setting `persist: true` when necessary
10. `analyze_recorded_traffic` / `query_recorded_traffic`

### 5.5 Call examples

Start a live capture:

```json
{
  "reset_session": true,
  "include_existing": false
}
```

Filter live API traffic:

```json
{
  "capture_id": "capture-id-from-start",
  "preset": "api_focus",
  "host_contains": "api.example.com",
  "max_items": 10
}
```

### 5.6 Caveats

- The `charles` MCP will not configure the Android system proxy for you; first set up Charles listening, the device proxy, and certificate preparation
- For real-time retrieval prefer `query_live_capture_entries`; don't default to `read_live_capture`, which advances the cursor
- `get_traffic_entry_detail` defaults to preview-only to save context; enable `include_full_body` only when the raw content is truly needed
- If you want to review the capture afterward, set `persist: true` when ending the live capture
- If Charles is already running and you don't want to clear the current session, use `adopt_existing: true`

---

## 6. `burp`: Burp Suite cooperative operations

### 6.1 Positioning

The `burp` MCP is a control and data-access layer for Burp Suite, suited for:

- Read proxy history
- Send requests to Repeater / Intruder
- Send HTTP/1.1 and HTTP/2 requests
- Generate Collaborator payloads
- View scanner issues
- Read/write current editor contents
- Adjust proxy interception and task-execution state
- Read/write Burp config

### 6.2 Method list

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__burp__base64_encode` | `content` | Base64 encode | Build a payload |
| `mcp__burp__base64_decode` | `content` | Base64 decode | Inspect encoded data |
| `mcp__burp__url_encode` | `content` | URL encode | Build parameters |
| `mcp__burp__url_decode` | `content` | URL decode | Restore parameters |
| `mcp__burp__generate_random_string` | `length`,`characterSet` | Generate a random string | Tokens, boundary values, probe strings |
| `mcp__burp__get_active_editor_contents` | none | Get current editor contents | Read a manually edited request |
| `mcp__burp__set_active_editor_contents` | `text` | Set current editor contents | Auto-fill a request template |
| `mcp__burp__create_repeater_tab` | `content`,`targetHostname`,`targetPort`,`usesHttps`,`tabName?` | Create a Repeater tab | Send a request to Repeater |
| `mcp__burp__send_to_intruder` | `content`,`targetHostname`,`targetPort`,`usesHttps`,`tabName?` | Send to Intruder | Brute-force / batch testing |
| `mcp__burp__send_http1_request` | `content`,`targetHostname`,`targetPort`,`usesHttps` | Send an HTTP/1.1 request | Precise replay |
| `mcp__burp__send_http2_request` | `pseudoHeaders`,`headers`,`requestBody`,`targetHostname`,`targetPort`,`usesHttps` | Send an HTTP/2 request | H2-specific scenarios |
| `mcp__burp__generate_collaborator_payload` | `customData?` | Generate an OOB domain | SSRF / RCE / Blind XXE testing |
| `mcp__burp__get_collaborator_interactions` | `payloadId?` | Poll OOB interactions | Check for outbound activity |
| `mcp__burp__get_proxy_http_history` | `count`,`offset` | Read proxy HTTP history | Review requests |
| `mcp__burp__get_proxy_http_history_regex` | `count`,`offset`,`regex` | Filter HTTP history by regex | Precise filtering |
| `mcp__burp__get_proxy_websocket_history` | `count`,`offset` | Read WS history | Analyze WebSocket |
| `mcp__burp__get_proxy_websocket_history_regex` | `count`,`offset`,`regex` | Filter WS history by regex | Look for tokens, command fields |
| `mcp__burp__get_scanner_issues` | `count`,`offset` | List scanner findings | Vulnerability review |
| `mcp__burp__output_project_options` | none | Export project-level config | View config schema |
| `mcp__burp__output_user_options` | none | Export user-level config | View config schema |
| `mcp__burp__set_project_options` | `json` | Set project-level config | Automated tuning |
| `mcp__burp__set_user_options` | `json` | Set user-level config | User-global configuration |
| `mcp__burp__set_proxy_intercept_state` | `intercepting` | Toggle proxy interception | Turn Intercept on/off |
| `mcp__burp__set_task_execution_engine_state` | `running` | Toggle the task-execution engine | Pause/resume scan tasks |

### 6.3 Typical call examples

Create a Repeater:

```json
{
  "content": "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
  "targetHostname": "example.com",
  "targetPort": 443,
  "usesHttps": true,
  "tabName": "home"
}
```

Generate a Collaborator payload:

```json
{
  "customData": "ssrf-test"
}
```

### 6.4 Caveats

- `send_http2_request` keeps the request body and headers separate; do not put headers into the body
- Before changing config, run `output_project_options` / `output_user_options` first
- OOB detection is generally: `generate_collaborator_payload` -> inject into a business point -> `get_collaborator_interactions`
- `get_proxy_http_history_regex` is well suited for "automatically filtering relevant history requests" in a skill

---

## 7. `chrome_devtools`: Browser automation, page diagnostics, and performance analysis

### 7.1 Positioning

`chrome_devtools` handles automated control of browser pages and DevTools-level observation. Core capabilities include:

- Open/close/select pages
- Navigate, refresh, emulate devices
- DOM snapshots, screenshots
- Click, type, upload files
- List network requests and console information
- Execute page scripts
- Lighthouse audit
- Performance trace
- Heap snapshots

If you want to "operate a page like a human in a browser," it is the first choice.

### 7.2 Page and context control

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__list_pages` | none | List currently open pages |
| `mcp__chrome_devtools__new_page` | `url`,`background?`,`isolatedContext?`,`timeout?` | Create a new tab and visit a URL |
| `mcp__chrome_devtools__select_page` | `pageId`,`bringToFront?` | Switch the active page |
| `mcp__chrome_devtools__close_page` | `pageId` | Close a page |
| `mcp__chrome_devtools__navigate_page` | `type`,`url?`,`timeout?`,`ignoreCache?`,`handleBeforeUnload?`,`initScript?` | URL navigation, forward, back, refresh |
| `mcp__chrome_devtools__resize_page` | `width`,`height` | Resize the browser |
| `mcp__chrome_devtools__emulate` | `viewport?`,`colorScheme?`,`geolocation?`,`networkConditions?`,`userAgent?`,`cpuThrottlingRate?` | Device/network/UA emulation |

### 7.3 Page structure and screenshots

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__take_snapshot` | `filePath?`,`verbose?` | Take a page a11y-tree snapshot, returning element `uid`s |
| `mcp__chrome_devtools__take_screenshot` | `filePath?`,`format?`,`fullPage?`,`quality?`,`uid?` | Screenshot a page or element |
| `mcp__chrome_devtools__wait_for` | `text`,`timeout?` | Wait for certain text to appear |

Notes:

- First `take_snapshot`, then use its `uid` for click/fill/hover; this is usually the most reliable
- `uid` is the element identifier within the current snapshot context and may change after the snapshot updates

### 7.4 Page interaction

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__click` | `uid`,`dblClick?`,`includeSnapshot?` | Click an element |
| `mcp__chrome_devtools__hover` | `uid`,`includeSnapshot?` | Hover an element |
| `mcp__chrome_devtools__drag` | `from_uid`,`to_uid`,`includeSnapshot?` | Drag |
| `mcp__chrome_devtools__fill` | `uid`,`value`,`includeSnapshot?` | Fill a single input |
| `mcp__chrome_devtools__fill_form` | `elements`,`includeSnapshot?` | Batch-fill a form |
| `mcp__chrome_devtools__type_text` | `text`,`submitKey?` | Type text into the current focus |
| `mcp__chrome_devtools__press_key` | `key`,`includeSnapshot?` | Keyboard shortcuts, special keys |
| `mcp__chrome_devtools__upload_file` | `uid`,`filePath`,`includeSnapshot?` | Upload a file |
| `mcp__chrome_devtools__handle_dialog` | `action`,`promptText?` | Handle alert/confirm/prompt |

### 7.5 Page scripts and debug info

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__evaluate_script` | `function`,`args?` | Execute JS in the page |
| `mcp__chrome_devtools__list_console_messages` | `includePreservedMessages?`,`pageIdx?`,`pageSize?`,`types?` | View console logs |
| `mcp__chrome_devtools__get_console_message` | `msgid` | Get details of a single console message |
| `mcp__chrome_devtools__list_network_requests` | `includePreservedRequests?`,`pageIdx?`,`pageSize?`,`resourceTypes?` | View the network request list |
| `mcp__chrome_devtools__get_network_request` | `reqid?`,`requestFilePath?`,`responseFilePath?` | View or export request details/body |

### 7.6 Audit and performance

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__lighthouse_audit` | `device?`,`mode?`,`outputDirPath?` | Run Lighthouse (excluding the performance score) |
| `mcp__chrome_devtools__performance_start_trace` | `autoStop?`,`filePath?`,`reload?` | Start a performance trace |
| `mcp__chrome_devtools__performance_stop_trace` | `filePath?` | Stop the performance trace |
| `mcp__chrome_devtools__performance_analyze_insight` | `insightName`,`insightSetId` | Analyze a particular performance insight |
| `mcp__chrome_devtools__take_memory_snapshot` | `filePath` | Export a JS heap snapshot |

### 7.7 Recommended workflow

#### Page automation

1. `new_page`
2. `take_snapshot`
3. `click` / `fill` / `press_key`
4. `wait_for`
5. `take_screenshot`

#### Capturing page requests

1. `new_page`
2. Page interaction
3. `list_network_requests`
4. `get_network_request`

#### Performance troubleshooting

1. `navigate_page`
2. `performance_start_trace`
3. Operate the page or reload
4. `performance_stop_trace`
5. `performance_analyze_insight`

### 7.8 Caveats

- Prefer `take_snapshot` before doing DOM interactions
- After a page refresh, old `uid`s may no longer be usable
- When getting request/response bodies, use `requestFilePath` / `responseFilePath` to write them to files when needed
- If you care about "JS call chains and breakpoints," `js_reverse` is often a better fit than this

---

## 8. `context7`: Real-time documentation and example retrieval

### 8.1 Positioning

`context7` suits querying third-party libraries, frameworks, official docs, and code examples, especially the skill-writing case of "citing the latest official usage."

### 8.2 Methods

#### `mcp__context7__resolve_library_id`

- Purpose: first resolve a "library name" into a Context7-recognizable document ID
- Parameters:
  - `libraryName`
  - `query`
- Key returns:
  - `libraryId`
  - Library name
  - Description
  - number of snippets
  - source reputation
  - benchmark score

#### `mcp__context7__query_docs`

- Purpose: retrieve docs and examples based on an already-resolved `libraryId`
- Parameters:
  - `libraryId`
  - `query`

### 8.3 Recommended workflow

1. `resolve_library_id`
2. Choose the most suitable `libraryId`
3. `query_docs`

### 8.4 Example

First resolve:

```json
{
  "libraryName": "Next.js",
  "query": "App Router middleware authentication examples"
}
```

Then query:

```json
{
  "libraryId": "/vercel/next.js",
  "query": "How to protect routes in App Router middleware?"
}
```

### 8.5 Caveats when writing a skill

- If the user gives a vague library name, run `resolve_library_id` first
- This is a "documentation Q&A MCP," not a free-form web search
- For technical questions, treat it primarily as an "official documentation retriever"

---

## 9. `everything_search`: Ultra-fast local file search

### 9.1 Positioning

This is a Windows local file-search MCP, suited for quickly finding files in large directories, across the whole disk, and under fuzzy conditions.

### 9.2 Methods

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__everything_search__search` | `query`,`maxResults?`,`parentPath?`,`filesOnly?`,`foldersOnly?`,`matchPath?`,`regex?`,`caseSensitive?`,`wholeWord?`,`sortBy?`,`sortDescending?`,`showSize?`,`showDateModified?` | Search for files or directories |
| `mcp__everything_search__get_file_info` | `filename` | Get detailed info about a file |

### 9.3 Example

Search for all `.apk` files under a given directory:

```json
{
  "query": "*.apk",
  "parentPath": "C:\\Users\\28484",
  "filesOnly": true,
  "maxResults": 50
}
```

### 9.4 Applicable scenarios

- Find APK / .so / logs / exported files
- Find target files for reversing skills
- Find configs, scripts, databases, certificates in large directories

---

## 10. `fetch`: General web page fetching

### 10.1 Positioning

`fetch` is a general tool for "fetching web page / URL content," suited for:

- Fetch web page content
- Fetch documentation pages
- Read HTML
- Do simple web page content extraction

### 10.2 Methods

#### `mcp__fetch__fetch`

- Parameters:
  - `url`
  - `max_length?`
  - `raw?`
  - `start_index?`
- Purpose:
  - Get web page content
  - Can return simplified markdown-style content
  - Can specify an offset to keep reading a long page

### 10.3 Example

```json
{
  "url": "https://example.com",
  "max_length": 6000
}
```

### 10.4 Caveats

- Better for "fetching content from a known URL," not a search engine
- If the page is too long, read it in slices via `start_index`
- In technical-documentation scenarios, if `context7` is available, prefer it

---

## 11. `frida_mcp`: Android dynamic injection and runtime hooking

### 11.1 Positioning

`frida_mcp` is the Android dynamic-analysis layer; core uses:

- Check/start/stop `frida-server`
- Enumerate applications
- Get the current foreground application
- `spawn` or `attach` to the target process
- Inject Frida JS scripts
- Get script output logs

Suitable scenarios:

- SSL pinning bypass
- Print method parameters/return values
- Dynamically capture signatures, tokens, headers
- native/Java-layer runtime observation

### 11.2 Method list

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__frida_mcp__check_frida_status` | none | Check whether frida-server is running | Pre-flight check |
| `mcp__frida_mcp__start_frida_server` | none | Start frida-server | Dynamic-analysis preparation |
| `mcp__frida_mcp__stop_frida_server` | none | Stop frida-server | Clean up the environment |
| `mcp__frida_mcp__list_applications` | none | List device applications | Find package names, see what is running |
| `mcp__frida_mcp__get_frontmost_application` | none | Get the current foreground app | Confirm the package name of the current screen |
| `mcp__frida_mcp__spawn` | `package_name`,`initial_script?`,`script_file_path?`,`output_file?` | Start suspended and attach to the target app | Early-timing hook |
| `mcp__frida_mcp__attach` | `target`,`initial_script?`,`script_file_path?`,`output_file?` | Attach to a PID or package name | Inject into an already-running app |
| `mcp__frida_mcp__get_messages` | `max_messages?` | Get the hook/log output buffer | See script print output |

### 11.3 Difference between `attach` and `spawn`

- `attach`
  - Used when the target is already running
  - Can attach by PID or package name
  - Suited for ad hoc observation and late hooking

- `spawn`
  - Used to inject a script before the app resumes
  - Suited for early class loading, startup flow, signature initialization, early SSL-pinning bypass

### 11.4 Example

Check status:

```json
{}
```

Start by package name and inject a script file:

```json
{
  "package_name": "com.example.app",
  "script_file_path": "C:\\Users\\28484\\Desktop\\hook.js",
  "output_file": "C:\\Users\\28484\\Desktop\\frida.log"
}
```

Attach to a running app and write an inline script directly:

```json
{
  "target": "com.example.app",
  "initial_script": "Java.perform(function(){ console.log('hook loaded'); });"
}
```

### 11.5 Recommended workflow

1. `check_frida_status`
2. If it is not running, `start_frida_server`
3. `list_applications` or `get_frontmost_application`
4. `spawn` or `attach`
5. `get_messages`

### 11.6 Caveats

- Requires `frida-server` correctly deployed in the device environment
- `script_file_path` takes priority over `initial_script`
- Most signing/crypto location tasks are usually: `jadx` static location -> `frida_mcp` dynamic verification

---

## 12. `ida_pro_mcp`: IDA Pro static analysis and batch refactoring

### 12.1 Positioning

`ida_pro_mcp` is the heaviest static-analysis MCP among the current capabilities. It is not "just decompilation"; it covers:

- Open/switch IDA instances
- Quickly survey the binary
- List functions, globals, imports, types
- Query xrefs / callgraph / basic blocks
- Decompile, disassemble, export function info
- Modify comments, rename, declare types, create stack variables
- Read memory, patch bytes, patch assembly
- Run scripts in the IDA context with Python

If a skill targets native reversing, malware analysis, patching, or batch renaming, it is almost the core.

### 12.2 Strongly recommended entry tools

#### `mcp__ida_pro_mcp__survey_binary`

This is the best tool for the first triage step. It can give you, in one call:

- File metadata
- Segment layout
- Entry point
- Statistics
- High-frequency strings
- High-value functions
- import categorization
- Call-graph overview

When writing a skill, you can specify explicitly:
"After you start analyzing the IDB, call `survey_binary` first; don't blindly call `list_funcs` directly."

### 12.3 Instance and session management

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__list_instances` | none | List currently connectable IDA instances |
| `mcp__ida_pro_mcp__select_instance` | `port`,`host?` | Switch the IDA instance the MCP points to |
| `mcp__ida_pro_mcp__open_file` | `file_path`,`autonomous?`,`new_database?`,`switch?`,`timeout?` | Open a file into a new IDA instance |
| `mcp__ida_pro_mcp__server_health` | none | Check current IDB/service health |
| `mcp__ida_pro_mcp__server_warmup` | `build_caches?`,`init_hexrays?`,`wait_auto_analysis?` | Warm up the analysis environment |
| `mcp__ida_pro_mcp__idb_save` | `path?` | Save the current IDB |

### 12.4 Binary overview and discovery

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__survey_binary` | `detail_level?` | Binary overview |
| `mcp__ida_pro_mcp__entity_query` | complex query object | Query functions/globals/imports/strings/names |
| `mcp__ida_pro_mcp__find_regex` | `pattern`,`limit?`,`offset?` | Search strings with regex |
| `mcp__ida_pro_mcp__find` | `targets`,`type`,`limit?`,`offset?` | Find strings, immediates, data/code references |
| `mcp__ida_pro_mcp__find_bytes` | `patterns`,`limit?`,`offset?` | Byte-pattern search |

### 12.5 Function and graph analysis

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__list_funcs` | `queries` | List functions |
| `mcp__ida_pro_mcp__func_query` | filter-condition set | Filter functions by size/name/whether they have types |
| `mcp__ida_pro_mcp__func_profile` | query set | Build an overview profile of a function |
| `mcp__ida_pro_mcp__lookup_funcs` | `queries` | Look up functions by address or name |
| `mcp__ida_pro_mcp__callees` | `addrs`,`limit?` | Query callee functions |
| `mcp__ida_pro_mcp__callgraph` | `roots`,`max_depth?`,`max_nodes?`,`max_edges?`,`max_edges_per_func?` | Build a call graph |
| `mcp__ida_pro_mcp__basic_blocks` | `addrs`,`offset?`,`max_blocks?` | Get CFG basic blocks |
| `mcp__ida_pro_mcp__analyze_function` | `addr`,`include_asm?` | Compact single-function analysis |
| `mcp__ida_pro_mcp__analyze_batch` | `queries` | Batch comprehensive multi-function analysis |
| `mcp__ida_pro_mcp__analyze_component` | `addrs` | Component analysis over a group of related functions |

### 12.6 Decompilation, disassembly, and export

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__decompile` | `addr` | Decompile a function |
| `mcp__ida_pro_mcp__disasm` | `addr`,`offset?`,`max_instructions?`,`include_total?` | Disassemble a function |
| `mcp__ida_pro_mcp__export_funcs` | `addrs`,`format?` | Export functions as JSON / C header / prototypes |

### 12.7 Cross-references and data flow

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__xrefs_to` | `addrs`,`limit?` | Get xrefs to |
| `mcp__ida_pro_mcp__xref_query` | query set | Batch-query xrefs by direction/type |
| `mcp__ida_pro_mcp__trace_data_flow` | `addr`,`direction?`,`max_depth?` | Trace multi-hop data flow |
| `mcp__ida_pro_mcp__xrefs_to_field` | `queries` | Query struct-field references |

### 12.8 Type system and structure recovery

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__type_query` | query set | Query local types |
| `mcp__ida_pro_mcp__type_inspect` | `queries` | Inspect type declarations and members |
| `mcp__ida_pro_mcp__declare_type` | `decls` | Inject C type declarations |
| `mcp__ida_pro_mcp__set_type` | `edits` | Set function/variable/local-variable types |
| `mcp__ida_pro_mcp__type_apply_batch` | `batch` | Batch-apply types |
| `mcp__ida_pro_mcp__infer_types` | `addrs` | Infer types |
| `mcp__ida_pro_mcp__enum_upsert` | `queries` | Create/augment enums |
| `mcp__ida_pro_mcp__search_structs` | `filter` | Search structs/unions |
| `mcp__ida_pro_mcp__read_struct` | `queries` | Read struct field values at an address |

### 12.9 Stack frames and local variables

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__stack_frame` | `addrs` | Get a function's stack frame |
| `mcp__ida_pro_mcp__declare_stack` | `items` | Declare stack variables |
| `mcp__ida_pro_mcp__delete_stack` | `items` | Delete stack variables |

### 12.10 Renaming, comments, and diff verification

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__rename` | `batch` | Batch-rename functions/data/locals/stack variables |
| `mcp__ida_pro_mcp__set_comments` | `items` | Set comments |
| `mcp__ida_pro_mcp__append_comments` | `items` | Append comments |
| `mcp__ida_pro_mcp__diff_before_after` | `addr`,`action`,`action_args` | Compare decompilation before and after applying rename/type/comment |

### 12.11 Raw memory reads and patching

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__get_bytes` | `regions` | Read bytes |
| `mcp__ida_pro_mcp__get_int` | `queries` | Read integers |
| `mcp__ida_pro_mcp__get_string` | `addrs` | Read strings |
| `mcp__ida_pro_mcp__get_global_value` | `queries` | Read global variable values |
| `mcp__ida_pro_mcp__put_int` | `items` | Write integers |
| `mcp__ida_pro_mcp__patch` | `patches` | Patch bytes |
| `mcp__ida_pro_mcp__patch_asm` | `items` | Patch assembly |
| `mcp__ida_pro_mcp__undefine` | `items` | Undefine back to raw bytes |
| `mcp__ida_pro_mcp__define_code` | `items` | Define bytes as code |
| `mcp__ida_pro_mcp__define_func` | `items` | Define a function |

### 12.12 Imports, globals, instructions, and entity queries

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__imports` | `count`,`offset` | List imports |
| `mcp__ida_pro_mcp__imports_query` | `queries` | Filter imports by module/name |
| `mcp__ida_pro_mcp__list_globals` | `queries` | List globals |
| `mcp__ida_pro_mcp__insn_query` | `queries` | Query instruction patterns |
| `mcp__ida_pro_mcp__int_convert` | `inputs` | Number format conversion |

### 12.13 Python extensions

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__py_eval` | `code` | Run a Python snippet in the IDA environment |
| `mcp__ida_pro_mcp__py_exec_file` | `file_path` | Run an entire Python script file |

### 12.14 Recommended workflow

#### Initial triage

1. `server_health`
2. `server_warmup`
3. `survey_binary`
4. `find_regex` / `imports_query`
5. `analyze_function` / `decompile`

#### Recovering semantics

1. `decompile`
2. `stack_frame`
3. `type_query` / `type_inspect`
4. `set_type` / `declare_type`
5. `rename`
6. `diff_before_after`

#### Tracing sensitive strings

1. `find_regex`
2. `xrefs_to`
3. `trace_data_flow`
4. `analyze_component`

### 12.15 Skill authoring advice

- Hard-coding "run `survey_binary` first" is usually a good strategy
- For batch renaming, treat `diff_before_after` as a verification step
- To analyze JNI / crypto / dispatch tables, `trace_data_flow` is very valuable
- `type_apply_batch` suits "auto-fix types" style skills
- `py_eval` / `py_exec_file` suit advanced automation, but define script boundaries carefully

---

## 13. `jadx`: APK static decompilation and Android code navigation

### 13.1 Positioning

The `jadx` MCP is the entry point for Android static analysis, suited for:

- Read `AndroidManifest.xml`
- Find the main Activity, components, and exported components
- Search classes/methods/fields
- Get class source, method source, smali
- Query reference relationships
- Rename classes/methods/fields/variables/packages

Its difference from `ida_pro_mcp` is:

- `jadx` leans toward the Java/Kotlin layer of an APK
- `ida_pro_mcp` leans toward native binaries / .so / ELF / PE

### 13.2 Entry information and Manifest

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__get_android_manifest` | none | Get the full Manifest |
| `mcp__jadx__get_main_activity_class` | none | Get the main Activity |
| `mcp__jadx__get_main_application_classes_names` | none | Get the main class names under the main application package |
| `mcp__jadx__get_main_application_classes_code` | `count?`,`offset?` | Get the code of the main classes |
| `mcp__jadx__get_manifest_component` | `component_type`,`only_exported?` | Get activity/service/provider/receiver component info |

### 13.3 Reading classes and source code

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__get_all_classes` | `count?`,`offset?` | Get all class names |
| `mcp__jadx__fetch_current_class` | none | Get the source of the class currently selected in the GUI |
| `mcp__jadx__get_class_source` | `class_name` | Get a class's Java source |
| `mcp__jadx__get_smali_of_class` | `class_name` | Get a class's smali |
| `mcp__jadx__get_methods_of_class` | `class_name` | List methods |
| `mcp__jadx__get_fields_of_class` | `class_name` | List fields |
| `mcp__jadx__get_method_by_name` | `class_name`,`method_name` | Get a method's source |
| `mcp__jadx__get_selected_text` | none | Get the currently selected text |

### 13.4 Resources and strings

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__get_all_resource_file_names` | `count?`,`offset?` | List resource files |
| `mcp__jadx__get_resource_file` | `resource_name` | Read resource file content |
| `mcp__jadx__get_strings` | `count?`,`offset?` | Get strings.xml content |

### 13.5 Search and references

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__search_classes_by_keyword` | `search_term`,`package?`,`search_in?`,`offset?`,`count?` | Cross-code search of classes/methods/fields/code content |
| `mcp__jadx__search_method_by_name` | `method_name` | Search for a method name |
| `mcp__jadx__get_xrefs_to_class` | `class_name`,`count?`,`offset?` | Query class references |
| `mcp__jadx__get_xrefs_to_field` | `class_name`,`field_name`,`count?`,`offset?` | Query field references |
| `mcp__jadx__get_xrefs_to_method` | `class_name`,`method_name`,`count?`,`offset?` | Query method references |

### 13.6 Renaming

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__rename_class` | `class_name`,`new_name` | Rename a class |
| `mcp__jadx__rename_field` | `class_name`,`field_name`,`new_name` | Rename a field |
| `mcp__jadx__rename_method` | `method_name`,`new_name` | Rename a method |
| `mcp__jadx__rename_variable` | `class_name`,`method_name`,`variable_name`,`new_name`,`reg?`,`ssa?` | Rename a variable |
| `mcp__jadx__rename_package` | `old_package_name`,`new_package_name` | Rename a package |

### 13.7 Debugging-related

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__debug_get_threads` | none | View debug threads |
| `mcp__jadx__debug_get_stack_frames` | none | View the current call stack |
| `mcp__jadx__debug_get_variables` | none | View current variables |

### 13.8 Recommended workflow

#### Preliminary APK analysis

1. `get_android_manifest`
2. `get_main_activity_class`
3. `get_manifest_component`
4. `search_classes_by_keyword`
5. `get_class_source`

#### Signing / API location

1. `search_classes_by_keyword` for `okhttp`, `retrofit`, `sign`, `token`, `encrypt`
2. `get_xrefs_to_method`
3. `get_method_by_name`
4. Switch to `frida_mcp` for dynamic verification when needed

### 13.9 Caveats

- `search_classes_by_keyword` is a very high-value entry tool in `jadx`
- `search_in` can specify `class,method,field,code,comment`
- For JNI scenarios, `jadx` usually finds the native registration point and `ida_pro_mcp` digs into the .so

---

## 14. `js_reverse`: Web front-end JavaScript reversing and breakpoint debugging

### 14.1 Positioning

`js_reverse` is a specialized MCP for web front-end reversing. Its difference from `chrome_devtools`:

- `chrome_devtools` leans toward page operations, network, snapshots, and performance
- `js_reverse` leans toward JS source, breakpoints, call chains, XHR initiators, function tracing, and source saving

Applicable scenarios:

- Analyze the signing function
- Trace the XHR/Fetch initiation chain
- Locate obfuscated functions
- Search for keywords in JS source
- Read variables within the execution context
- Analyze WebSocket message patterns

### 14.2 Pages and context

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__new_page` | `url`,`timeout?` | Create a new page |
| `mcp__js_reverse__select_page` | `pageIdx?` | List or switch pages |
| `mcp__js_reverse__navigate_page` | `type`,`url?`,`timeout?`,`ignoreCache?` | Navigate/refresh |
| `mcp__js_reverse__select_frame` | `frameIdx?` | List or switch frame/iframe |

### 14.3 Script enumeration and source reading

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__list_scripts` | `filter?` | List the current page's scripts |
| `mcp__js_reverse__search_in_sources` | `query`,`isRegex?`,`caseSensitive?`,`excludeMinified?`,`urlFilter?`,`maxResults?`,`maxLineLength?` | Search across all scripts |
| `mcp__js_reverse__get_script_source` | `url?`,`scriptId?`,`startLine?`,`endLine?`,`offset?`,`length?` | Read a small source slice |
| `mcp__js_reverse__save_script_source` | `filePath`,`url?`,`scriptId?` | Save the full script locally |

Notes:

- `get_script_source` is designed for "viewing a local slice," not pulling the whole file
- Large scripts should use `save_script_source`

### 14.4 Breakpoints, tracing, and execution control

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__set_breakpoint_on_text` | `text`,`urlFilter?`,`occurrence?`,`condition?` | Auto-set a breakpoint by code text |
| `mcp__js_reverse__list_breakpoints` | none | List breakpoints |
| `mcp__js_reverse__remove_breakpoint` | `breakpointId?`,`url?` | Remove a breakpoint or XHR breakpoint |
| `mcp__js_reverse__pause_or_resume` | none | Pause or resume execution |
| `mcp__js_reverse__step` | `direction` | Single-step over/into/out |
| `mcp__js_reverse__trace_function` | `functionName`,`logArgs?`,`logThis?`,`pause?`,`traceId?`,`urlFilter?` | Trace function calls |
| `mcp__js_reverse__inject_before_load` | `script?`,`identifier?` | Inject a script before the page loads |

### 14.5 Context analysis after a breakpoint hits

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__get_paused_info` | `frameIndex?`,`includeScopes?`,`maxScopeDepth?` | Get the stack and scope variables at a breakpoint hit |
| `mcp__js_reverse__evaluate_script` | `function`,`frameIndex?`,`mainWorld?` | Execute JS in the current page or a breakpoint frame |

### 14.6 Network and call chains

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__break_on_xhr` | `url` | Set a breakpoint on XHR/Fetch containing the target URL |
| `mcp__js_reverse__list_network_requests` | `reqid?`,`pageIdx?`,`pageSize?`,`resourceTypes?`,`urlFilter?`,`includePreservedRequests?` | View the request list or a single request's details |
| `mcp__js_reverse__get_request_initiator` | `requestId` | See which JS initiated a request |
| `mcp__js_reverse__list_console_messages` | `msgid?`,`pageIdx?`,`pageSize?`,`types?`,`includePreservedMessages?` | View the console |

### 14.7 WebSocket analysis

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__get_websocket_messages` | `wsid?`,`analyze?`,`groupId?`,`frameIndex?`,`direction?`,`show_content?`,`pageIdx?`,`pageSize?`,`urlFilter?`,`includePreservedConnections?` | List WS connections, analyze message groups, view specific frames |

### 14.8 Screenshots

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__take_screenshot` | `filePath?`,`format?`,`fullPage?`,`quality?` | Screenshot |

### 14.9 Recommended workflow

#### Locating the signing function

1. `new_page`
2. `list_scripts`
3. `search_in_sources` for `sign` / `token` / path keywords
4. `set_breakpoint_on_text`
5. Trigger the request
6. `get_paused_info`
7. `step`
8. `evaluate_script`

#### Tracing who initiated a request

1. Operate the page
2. `list_network_requests`
3. `get_request_initiator`
4. `break_on_xhr` when needed

#### Analyzing obfuscated scripts

1. `search_in_sources`
2. `save_script_source`
3. `set_breakpoint_on_text`
4. `trace_function`

### 14.10 Skill authoring advice

- When you have a source keyword, prefer `search_in_sources`
- When you have a request URL, prefer `break_on_xhr` or `get_request_initiator`
- When you need global variables in the page script scope, consider `mainWorld: true`
- If the page reloads frequently, look up scripts by URL rather than over-relying on ephemeral `scriptId`s

---

## 15. `memory`: Structured knowledge-graph memory

### 15.1 Positioning

`memory` is a long-term structured memory layer, not ordinary notes. It maintains an "entity-observation-relation" knowledge graph.

Suited for:

- Record user preferences
- Record project facts
- Record structured knowledge such as devices, targets, package names, API names, vulnerability points
- Persist stable facts across multi-turn tasks

### 15.2 Core objects

- Entity `entity`
  - Has a name `name`
  - Has a type `entityType`
  - Has multiple observations `observations`

- Relation `relation`
  - `from`
  - `relationType`
  - `to`

### 15.3 Method list

| Tool | Main parameters | Purpose |
| --- | --- | --- |
| `mcp__memory__read_graph` | none | Read the entire graph |
| `mcp__memory__search_nodes` | `query` | Search entities/types/observations |
| `mcp__memory__open_nodes` | `names` | Open details of specified entities |
| `mcp__memory__create_entities` | `entities` | Batch-create entities |
| `mcp__memory__delete_entities` | `entityNames` | Delete entities |
| `mcp__memory__add_observations` | `observations` | Append observations to an entity |
| `mcp__memory__delete_observations` | `deletions` | Delete observations |
| `mcp__memory__create_relations` | `relations` | Create relations |
| `mcp__memory__delete_relations` | `relations` | Delete relations |

### 15.4 Example

Create entities:

```json
{
  "entities": [
    {
      "name": "com.example.app",
      "entityType": "android_app",
      "observations": [
        "main package name",
        "uses OkHttp"
      ]
    }
  ]
}
```

Create relations:

```json
{
  "relations": [
    {
      "from": "com.example.app",
      "relationType": "uses",
      "to": "OkHttp"
    }
  ]
}
```

### 15.5 Uses suited to skills

- In a reversing skill, remember the target package name, crypto classes, .so names, key APIs
- In a pentest skill, remember domains, vulnerability points, scan results
- In an automation skill, remember account environments, deployment methods, agreed paths

### 15.6 Caveats

- State relations in the active voice, e.g. `App uses OkHttp`
- Not suited for storing very long raw text; better for storing "searchable facts"

---

## 16. `sequential_thinking`: Step-by-step thinking aid

### 16.1 Positioning

This is an "explicit multi-step thinking" tool, for analyzing complex problems, correcting, branching, and verifying hypotheses.
It is suited for:

- Planning multi-step reverse-engineering analysis
- Solution exploration for uncertain tasks
- Complex decisions that require correcting an earlier judgment
- Decomposing large tasks

### 16.2 Methods

#### `mcp__sequential_thinking__sequentialthinking`

Main parameters:

- `thought`
- `thoughtNumber`
- `totalThoughts`
- `nextThoughtNeeded`
- `isRevision?`
- `revisesThought?`
- `branchFromThought?`
- `branchId?`
- `needsMoreThoughts?`

### 16.3 Understanding how to use it

This tool is not for "looking up data" but for submitting reasoning state to the system in a structured way.
You can:

- Start analysis from step 1
- Revise when you find an earlier step was wrong
- Branch from a particular step
- Finally arrive at a verified solution

### 16.4 Scenarios suited to skills

- Automated triage skill
- Deciding on a multi-stage exploitation route
- The "Java first or native first" decision in reversing
- Filtering among multiple candidate signing functions

### 16.5 Example

```json
{
  "thought": "First determine whether the 403 is caused by front-end signing or server-side validation.",
  "thoughtNumber": 1,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}
```

### 16.6 Caveats

- This is an analysis enhancer, not an executor
- No need to use it for simple tasks
- Especially valuable for complex, ambiguous problems that are easy to get wrong

---

## 17. `scrcpy_vision`: Android visual control, UI location, and wireless debugging

### 17.1 Positioning

`scrcpy_vision` integrates ADB, low-latency scrcpy control, screen capture/streaming, and `uiautomator` UI-tree reading into one tool set, suited for:

- `serial`-centric Android device connection and identification
- UI location based on the current page's element text, `resource-id`, and `content-desc`
- Coordinate taps, drags, long-presses, swipes, keyboard input
- Confirm state such as screen wake/unlock, foreground Activity, notifications, clipboard
- USB-to-WiFi ADB debugging
- Single-frame screenshots or a continuous stream, for observing UI changes and automation coordination

Compared with `adb_mcp`, it leans toward "visual control" and "UI-layer location"; `adb_mcp` leans toward basic device management, APK install, logcat, screen recording, and file transfer. In skills the two are usually complementary rather than either/or.

### 17.2 Suitable skill types

- Android UI automation and page regression
- Element location and UI driving in app dynamic testing
- Wireless-debugging switching and remote control of a physical device
- Verify page state before and after capture/hook
- Tasks that need to confirm the position of buttons, input fields, and dialogs via the UI tree
- Tasks that need to watch the device screen continuously rather than take a single screenshot

### 17.3 Method list

#### Device connection and identification

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_devices_list` | none | List connected devices | Get the `serial`, confirm the USB/WiFi connection is healthy |
| `mcp__scrcpy_vision__android_devices_info` | `serial` | Read basic device `getprop` info | See model, OS version, ABI, device identifiers |
| `mcp__scrcpy_vision__android_adb_enableTcpip` | `serial`,`port?` | Enable WiFi debugging while connected over USB | Prepare for wireless ADB |
| `mcp__scrcpy_vision__android_adb_getDeviceIp` | `serial` | Get the device's WiFi IP | Prepare for `connectWifi` |
| `mcp__scrcpy_vision__android_adb_connectWifi` | `ipAddress`,`port?` | Connect to the device over WiFi | Wireless debugging |
| `mcp__scrcpy_vision__android_adb_disconnectWifi` | `ipAddress?` | Disconnect a specific or all WiFi ADB connections | Clean up wireless-debug sessions |

#### Applications and runtime state

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_app_start` | `serial`,`packageName`,`activity?` | Start an app or a specific Activity | Open the target app, jump directly to a page |
| `mcp__scrcpy_vision__android_app_stop` | `serial`,`packageName` | Force-stop an app | Reset the app state |
| `mcp__scrcpy_vision__android_apps_list` | `serial`,`system?` | List installed packages | Find package names, confirm whether an app is installed |
| `mcp__scrcpy_vision__android_activity_current` | `serial` | Get the current foreground package and Activity | Determine whether the page switched successfully |
| `mcp__scrcpy_vision__android_notifications_get` | `serial` | Export current notification details | Inspect verification-code notifications, push copy, source package |

#### Screen, clipboard, and device state

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_screen_isOn` | `serial` | Determine whether the screen is on | Check device state before automation |
| `mcp__scrcpy_vision__android_screen_wake` | `serial` | Turn on the screen | Prepare to operate the device |
| `mcp__scrcpy_vision__android_screen_sleep` | `serial` | Turn off the screen | Wrap-up or verify lock-screen behavior |
| `mcp__scrcpy_vision__android_screen_unlock` | `serial` | Attempt to wake and unlock the device | Quickly reach the home screen when there is no security lock |
| `mcp__scrcpy_vision__android_clipboard_get` | `serial` | Read clipboard content | Get verification codes, share links, copied results |
| `mcp__scrcpy_vision__android_clipboard_set` | `serial`,`text` | Attempt to set the clipboard | Paste prepared text into an input field |

#### Files and shell

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_file_list` | `serial`,`path` | List device directory contents | Inspect export, cache, and download directories |
| `mcp__scrcpy_vision__android_file_pull` | `serial`,`remotePath`,`localPath` | Pull a file from the device to local | Export logs, images, downloaded files |
| `mcp__scrcpy_vision__android_file_push` | `serial`,`localPath`,`remotePath` | Push a local file to the device | Push configs, test files, certificates |
| `mcp__scrcpy_vision__android_shell_exec` | `serial`,`command` | Run an arbitrary `adb shell` command | Advanced diagnostics, resolution queries, or device operations when necessary |

#### UI-tree reading and input control

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_ui_dump` | `serial` | Export the current page's `uiautomator` XML | Get element text, class names, bounds, `resource-id` |
| `mcp__scrcpy_vision__android_ui_findElement` | `serial`,`text?`,`resourceId?`,`className?`,`contentDesc?` | Find an element by UI attributes and return its center coordinate | Locate buttons, input fields, dialog controls |
| `mcp__scrcpy_vision__android_input_tap` | `serial`,`x`,`y` | Tap a coordinate | Tap buttons, list items, menus |
| `mcp__scrcpy_vision__android_input_longPress` | `serial`,`x`,`y`,`durationMs?` | Long-press a coordinate | Bring up a context menu, prepare a drag |
| `mcp__scrcpy_vision__android_input_swipe` | `serial`,`x1`,`y1`,`x2`,`y2`,`durationMs?` | Swipe the screen | Scroll lists, switch pages, pull to refresh |
| `mcp__scrcpy_vision__android_input_dragDrop` | `serial`,`startX`,`startY`,`endX`,`endY`,`durationMs?` | Drag to a target position | Drag cards, icons, sortable items |
| `mcp__scrcpy_vision__android_input_pinch` | `serial`,`centerX`,`centerY`,`startDistance`,`endDistance`,`durationMs?` | Approximate a pinch-zoom gesture | Map and image zoom verification |
| `mcp__scrcpy_vision__android_input_keyevent` | `serial`,`keycode` | Send an Android key | Home, Back, Enter, Delete, volume keys |
| `mcp__scrcpy_vision__android_input_text` | `serial`,`text` | Input text | Login, search, form filling |

#### Vision capabilities

| Tool | Main parameters | Purpose | Typical use |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_vision_snapshot` | `serial` | Capture the current screen as PNG via `adb exec-out screencap -p` | Single screenshot to confirm the UI |
| `mcp__scrcpy_vision__android_vision_startStream` | `serial`,`frameFps?`,`maxFps?`,`maxSize?` | Start a continuous scrcpy+ffmpeg stream | Continuously observe page changes, paired with fast input control |
| `mcp__scrcpy_vision__android_vision_stopStream` | `serial` | Stop the stream and release resources | Wrap-up, free stream resources |

### 17.4 Recommended workflow

#### Page automation and location

1. `android_devices_list`
2. `android_screen_isOn` / `android_screen_wake` / `android_screen_unlock`
3. If you will use coordinate taps or swipes later, first run `wm size` via `android_shell_exec` to get the current resolution
4. `android_vision_snapshot` or `android_vision_startStream`
5. `android_ui_dump` or `android_ui_findElement`
6. `android_input_tap` / `android_input_text` / `android_input_swipe`
7. `android_activity_current` to confirm whether the target page was reached
8. Keep the stream while continuous observation is needed, and `android_vision_stopStream` when done

#### Switching to WiFi ADB

1. After connecting the device over USB, run `android_adb_enableTcpip`
2. `android_adb_getDeviceIp`
3. `android_adb_connectWifi`
4. `android_devices_list` to confirm the wireless connection has appeared
5. After testing, clean up with `android_adb_disconnectWifi`

### 17.5 Call examples

Enable WiFi debugging:

```json
{
  "serial": "R58N123456A",
  "port": 5555
}
```

Find an element by text:

```json
{
  "serial": "R58N123456A",
  "text": "login"
}
```

Start a continuous stream:

```json
{
  "serial": "R58N123456A",
  "frameFps": 5,
  "maxSize": 1080
}
```

Query the current resolution:

```json
{
  "serial": "R58N123456A",
  "command": "wm size"
}
```

### 17.6 Caveats

- Except for `android_devices_list`, `android_adb_connectWifi`, and `android_adb_disconnectWifi`, most methods require obtaining the device `serial` first
- If the scrcpy stream is running, taps, swipes, and input go through the faster scrcpy control channel first; otherwise they fall back to ADB input
- Before sending coordinate taps, long-presses, swipes, drags, or pinches, query the current resolution first; different devices, orientation, scaling, or screenshot-size assumptions can all cause coordinate drift
- `android_ui_findElement` suits static location on the current page; after the page changes, re-run `ui_dump` or re-query the element
- Prefer `android_ui_findElement` / `android_ui_dump` over hard-coded coordinates; fall back to coordinate taps only when element location is unreliable
- `android_screen_unlock` only works on devices with no security lock such as a PIN/password/pattern
- `android_clipboard_set` may be restricted by the system on Android 10+ and is not guaranteed to work directly on every device
- `android_input_pinch` is an approximate gesture, not true multi-touch
- `android_shell_exec` and `android_file_push` directly modify the device environment; a skill should state clearly that these are high-risk operations
- `android_vision_startStream` produces a live resource rather than a saved file; for a single screenshot, prefer `android_vision_snapshot`

---

## 18. Recommended grouping for skill authoring

For writing skills later, it is better to organize by "task domain" rather than mechanically splitting by "tool server name."

### 18.1 Android static-analysis skill

Preferred MCP:

- `jadx`
- `everything_search`

Common workflow:

1. Find the APK / resources
2. Read the Manifest
3. Search for key classes
4. Pull the method source
5. Follow xrefs

### 18.2 Android dynamic-analysis skill

Preferred MCP:

- `adb_mcp`
- `scrcpy_vision`
- `frida_mcp`
- `charles`

Common workflow:

1. Confirm the device
2. Install the app
3. Start the scrcpy stream or read the UI tree as appropriate
4. Start the Charles live capture
5. Inject the hook
6. Inspect requests, UI, and logs

### 18.3 Native reversing skill

Preferred MCP:

- `ida_pro_mcp`
- `everything_search`

Common workflow:

1. Find the .so / .exe
2. `survey_binary`
3. Query strings/imports
4. Decompile key functions
5. Rename, fix types, follow data flow

### 18.4 Web page automation skill

Preferred MCP:

- `chrome_devtools`

Common workflow:

1. Open the page
2. Take a snapshot
3. Interact with the form
4. Capture the request
5. Screenshot for evidence

### 18.5 Web JS reversing skill

Preferred MCP:

- `js_reverse`
- `chrome_devtools`
- `burp`

Common workflow:

1. Search the source
2. Set a breakpoint on the request URL
3. Follow the call chain
4. Export the script
5. Burp replay

### 18.6 Documentation retrieval skill

Preferred MCP:

- `context7`
- `fetch`

Common workflow:

1. `resolve_library_id`
2. `query_docs`
3. If you need additional page content, then use `fetch`

---

## 19. Prompt templates you can reuse directly when writing skills

Below are a few templates suitable for adapting directly into skills.

### 19.1 Android reversing skill template snippet

```text
When the user asks to analyze an Android APK:
1. If the task is a pentest of an authorized Android app, don't statically analyze the APK first; first confirm whether the target app is already installed on the connected device.
2. First set up capture visibility in burp or charles, then use scrcpy_vision to open the app and drive real business clicks, input, and navigation.
3. After each key action, first check whether HTTP/HTTPS or WebSocket packets have appeared in burp or charles, and combine with adb_mcp to view logs, UI anomalies, and runtime state.
4. If packets are already visible and replayable, move directly to Web/API/WebSocket security testing, and keep advancing across business features in the loop "UI action -> packet -> web security analysis."
5. Only when packets can't be captured, are encrypted, plaintext is unavailable, the protocol is still opaque, replay is unstable, or anomalies clearly point to client-side logic blocking, use jadx to read AndroidManifest.xml, the main Activity, and exported components, and search for keywords such as okhttp/retrofit/sign/token/encrypt.
6. If the Java layer is still not enough, use frida_mcp to hook the Java or native boundary to recover plaintext; if native clues appear (System.loadLibrary, JNI, .so files) and Java plus hooking still can't resolve it, switch to ida_pro_mcp to analyze the dumped .so.
7. If you need to control the device, locate by UI element, watch the live screen, or switch to WiFi debugging, use scrcpy_vision; if you need to install apps, screen-record, logcat, or basic file transfer, use adb_mcp.
```

### 19.2 Web JS reversing skill template snippet

```text
When the user asks to locate a front-end signature, obfuscated function, or API call chain:
1. Prefer js_reverse to enumerate scripts and use search_in_sources to search for keywords such as sign/token/hash/encode/api path.
2. If the request URL is known, prefer break_on_xhr or get_request_initiator to determine where it is initiated.
3. For key functions, use set_breakpoint_on_text, trace_function, get_paused_info, step, and evaluate_script to obtain runtime context.
4. If you need to save the full script for offline analysis, use save_script_source.
5. If you need to reproduce or replay the request, use burp's create_repeater_tab, send_http1_request, send_http2_request.
6. If you need page-level interaction or screenshots, use chrome_devtools.
```

### 19.3 Native binary analysis skill template snippet

```text
When the user asks to analyze a binary, .so, malware sample, or patch point:
1. After opening IDA, call ida_pro_mcp.survey_binary first for an overview; don't blindly call list_funcs directly.
2. Prefer starting from strings, imports, callgraph, key constants, and sensitive APIs to narrow the scope.
3. For suspicious functions, use analyze_function / decompile / xref_query / trace_data_flow.
4. If a function is hard to read, use rename, set_type, declare_type, stack_frame, diff_before_after to recover its semantics step by step.
5. If you need to modify the sample, use patch / patch_asm / put_int, and save the IDB when necessary.
```

---

## 20. Summary of common caveats

### 20.1 Absolute-path requirements

The following kinds of tools often require absolute paths:

- `adb_mcp.take_screenshot`
- `adb_mcp.record_screen`
- `adb_mcp.pull_file` / `push_file`
- `scrcpy_vision.android_file_pull` / `android_file_push`
- `frida_mcp`'s `script_file_path` and `output_file`
- `js_reverse.save_script_source`
- `chrome_devtools.take_screenshot`
- `chrome_devtools.take_memory_snapshot`
- `ida_pro_mcp.open_file`

### 20.2 Pagination-type parameters

Common pagination/slicing parameters:

- `offset`
- `count`
- `limit`
- `pageIdx`
- `pageSize`
- `start_index`
- `length`

When writing a skill, it is advisable to state explicitly:

- By default, take a small batch of samples first
- If there are too many results, increase limit / count

### 20.3 Discover first, then dig deeper

Many MCPs have obvious "discovery-phase tools"; don't dig deep right away:

- `ida_pro_mcp`: `survey_binary`
- `jadx`: `get_android_manifest` / `search_classes_by_keyword`
- `js_reverse`: `list_scripts` / `search_in_sources`
- `chrome_devtools`: `take_snapshot`
- `charles`: `query_live_capture_entries`

### 20.4 Evidence retention

MCPs suited for evidence retention:

- `adb_mcp.take_screenshot`
- `adb_mcp.record_screen`
- `scrcpy_vision.android_vision_snapshot`
- `chrome_devtools.take_screenshot`
- `js_reverse.take_screenshot`
- `charles.get_traffic_entry_detail`
- `burp` history and Repeater

### 20.5 The most common combinations

- Android static + dynamic: `jadx` + `frida_mcp`
- Android dynamic + traffic: `adb_mcp` + `charles`
- Android dynamic + UI automation: `scrcpy_vision` + `frida_mcp`
- Android traffic capture + page driving: `scrcpy_vision` + `charles`
- Web automation + JS reversing: `chrome_devtools` + `js_reverse`
- Web security replay: `js_reverse` + `burp`
- Native static + dynamic: `ida_pro_mcp` + `frida_mcp`

---

## 21. Summary

If your goal is to "make it easy to write skills later," the most practical approach is not to write one skill per MCP but to split by task domain:

- Android static analysis
- Android dynamic analysis and traffic capture
- Web automation
- Web JS reversing
- Native binary analysis
- Documentation retrieval
- Memory and task-state management

The MCPs most worth designing skills around first are:

1. `jadx`
2. `ida_pro_mcp`
3. `js_reverse`
4. `chrome_devtools`
5. `frida_mcp`
6. `charles`
7. `adb_mcp`

If you want, I can also continue to do two more things on top of this document:

1. Then generate a "skill-friendly condensed MCP cheat sheet"
2. Split this document directly into multiple `SKILL.md` template skeletons
