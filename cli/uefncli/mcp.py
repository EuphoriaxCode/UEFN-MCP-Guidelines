"""Minimal streamable-HTTP MCP client for the UEFN editor server (http://127.0.0.1:8000/mcp).

The editor exposes three meta-tools: list_toolsets, describe_toolset, call_tool.
Session ids are cached on disk so consecutive CLI invocations reuse one MCP session.
"""
import json
import os
import tempfile
import time
import urllib.error
import urllib.request

URL = os.environ.get("UEFN_MCP_URL", "http://127.0.0.1:8000/mcp")
SID_FILE = os.path.join(tempfile.gettempdir(), "uefn_mcp_sid.txt")
TIMEOUT = float(os.environ.get("UEFN_MCP_TIMEOUT", "900"))


class McpError(RuntimeError):
    pass


def _post(body, sid=None, timeout=TIMEOUT):
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if sid:
        h["Mcp-Session-Id"] = sid
    req = urllib.request.Request(URL, json.dumps(body).encode("utf-8"), h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.headers.get("Mcp-Session-Id"), r.headers.get("Content-Type", ""), r.read().decode("utf-8", "replace")


def _parse(ctype, text):
    """Responses are plain JSON; fall back to the last SSE `data:` frame."""
    text = text.strip()
    if not text:
        return None
    if "text/event-stream" in ctype or text.startswith("event:") or text.startswith("data:"):
        last = None
        for line in text.splitlines():
            if line.startswith("data:"):
                last = line[5:].strip()
        text = last or "{}"
    return json.loads(text)


def _new_session():
    sid, ct, body = _post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                           "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                                      "clientInfo": {"name": "uefn-cli", "version": "1"}}}, timeout=30)
    if not sid:
        raise McpError("server did not return Mcp-Session-Id")
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid, timeout=30)
    with open(SID_FILE, "w") as f:
        f.write(sid)
    return sid


def session(force_new=False):
    if not force_new and os.path.exists(SID_FILE):
        with open(SID_FILE) as f:
            s = f.read().strip()
        if s:
            return s
    return _new_session()


_rid = int(time.time() * 1000) % 1000000


def request(method, params=None, timeout=TIMEOUT):
    """JSON-RPC request; retries once with a fresh session if the cached one is stale."""
    global _rid
    for attempt in (0, 1):
        sid = session(force_new=attempt == 1)
        _rid += 1
        try:
            _, ct, body = _post({"jsonrpc": "2.0", "id": _rid, "method": method, "params": params or {}}, sid, timeout)
        except urllib.error.HTTPError as e:
            if attempt == 0 and e.code in (400, 404, 410):
                continue
            raise McpError(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")
        except urllib.error.URLError as e:
            raise McpError(f"cannot reach UEFN MCP at {URL} ({e.reason}). Is the editor open with the project loaded?")
        j = _parse(ct, body)
        if j is None:
            raise McpError("empty response")
        if "error" in j:
            err = j["error"]
            msg = str(err.get("message", err))
            if attempt == 0 and ("session" in msg.lower()):
                continue
            raise McpError(msg)
        return j.get("result")
    raise McpError("request failed after session refresh")


def meta(name, arguments):
    """Call one of the three top-level meta tools; returns (texts, images, is_error)."""
    r = request("tools/call", {"name": name, "arguments": arguments})
    texts, images = [], []
    for c in r.get("content", []):
        if c.get("type") == "image":
            images.append(c)
        elif "text" in c:
            texts.append(c["text"])
    return texts, images, bool(r.get("isError"))
