#!/usr/bin/env python3
"""Baseline tests for the API Lessons MCP server (https://ll-mcp.replit.app/mcp).

Run after every Replit deploy, and whenever Emmanuel says "test the MCP server".

    python3 test-mcp-server.py

Exits 0 if all tests pass, 1 otherwise. Stdlib only, no auth required.

Tests:
  1. Deploy check   — server live, and the data it serves MATCHES sample-lightning-lessons.json
  2. Tool title     — top-level `title` is set (expected: "Get Lessons")
  3. outputSchema   — declared on the tool, and well-formed
  4. Output JSON    — tools/call returns structuredContent that CONFORMS to outputSchema
  5. Version        — serverInfo.version matches the version submitted to OpenAI

Test 1 compares against the canonical file rather than a hardcoded lesson count,
so it keeps working as lessons are added. If the file and server disagree, the
deploy did not land — deploy is Emmanuel's manual step in Replit.
"""

import json
import os
import sys
import urllib.request

URL = "https://ll-mcp.replit.app/mcp"
CANONICAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample-lightning-lessons.json")
EXPECTED_TITLE = "Get Lessons"
TOOL = "getLessons"

# The version submitted to OpenAI. The server must report the same on initialize —
# a mismatch means the Replit deploy is not the build that was submitted.
EXPECTED_VERSION = "2.0.0"

# Fields that must round-trip byte-identically from the file to the wire.
COMPARED_FIELDS = ["id", "title", "instructors", "guests", "url", "date",
                   "status", "courseName", "courseUrl", "description", "outcomes"]


def rpc(method, params=None, session=None, notify=False):
    """One JSON-RPC call over MCP streamable HTTP. Returns (result, session_id)."""
    body = {"jsonrpc": "2.0", "method": method}
    if not notify:
        body["id"] = 1
    if params is not None:
        body["params"] = params
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream",
                 **({"mcp-session-id": session} if session else {})},
        method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        sid = resp.headers.get("mcp-session-id") or session
        raw = resp.read().decode()
    if notify:
        return None, sid
    # Streamable HTTP frames responses as SSE: "data: {...}"
    for line in raw.splitlines():
        if line.startswith("data: "):
            msg = json.loads(line[6:])
            if "error" in msg:
                raise RuntimeError(f"{method} -> {msg['error']}")
            return msg.get("result"), sid
    raise RuntimeError(f"{method}: no data frame in response: {raw[:200]}")


def conforms(node, schema, path="$"):
    """Minimal JSON Schema check — enough for this tool's shape. Returns list of errors.

    Deliberately stdlib-only: `jsonschema` is not installed and this must never
    silently skip (a skipped check reads as a pass).
    """
    errs = []
    t = schema.get("type")
    types = {"object": dict, "array": list, "string": str,
             "number": (int, float), "integer": int, "boolean": bool}
    if t and t in types and not isinstance(node, types[t]):
        return [f"{path}: expected {t}, got {type(node).__name__}"]
    if t == "object":
        for req in schema.get("required", []):
            if req not in node:
                errs.append(f"{path}.{req}: required but missing")
        for key, sub in schema.get("properties", {}).items():
            if key in node:
                errs += conforms(node[key], sub, f"{path}.{key}")
    elif t == "array" and "items" in schema:
        for i, item in enumerate(node):
            errs += conforms(item, schema["items"], f"{path}[{i}]")
    return errs


def main():
    results = []

    def check(name, ok, detail=""):
        results.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
        return ok

    print(f"API Lessons MCP server — baseline tests\n  {URL}\n")

    # --- handshake ---
    try:
        info, sid = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                       "clientInfo": {"name": "baseline-tests", "version": "1"}})
        rpc("notifications/initialized", session=sid, notify=True)
        tools = rpc("tools/list", {}, session=sid)[0]["tools"]
        tool = next(t for t in tools if t["name"] == TOOL)
    except Exception as e:
        print(f"  FAIL  server reachable — {e}")
        print("\nRESULT: FAIL (server unreachable; cannot run tests)")
        return 1
    version = info["serverInfo"]["version"]
    print(f"  server: {info['serverInfo']['name']} v{version}\n")

    # --- Test 5: serverInfo.version matches what was submitted to OpenAI ---
    check(f"5. serverInfo.version == {EXPECTED_VERSION!r}", version == EXPECTED_VERSION,
          "" if version == EXPECTED_VERSION
          else f"got {version!r} — deployed build is not the submitted one")

    # --- Test 2: tool title ---
    title = tool.get("title")
    check("2. tool title is set", bool(title), f"title={title!r}")
    check(f"   title == {EXPECTED_TITLE!r}", title == EXPECTED_TITLE, "" if title == EXPECTED_TITLE
          else f"got {title!r}")

    # --- Test 3: outputSchema present ---
    oschema = tool.get("outputSchema")
    has_schema = check("3. outputSchema declared", oschema is not None)
    if has_schema:
        lessons_schema = oschema.get("properties", {}).get("lessons")
        check("   outputSchema describes a lessons[] array",
              bool(lessons_schema) and lessons_schema.get("type") == "array")

    # --- call the tool once, reused by tests 1 and 4 ---
    try:
        res = rpc("tools/call", {"name": TOOL, "arguments": {"query": "all"}}, session=sid)[0]
    except Exception as e:
        check("1. deploy check", False, f"tools/call failed: {e}")
        print("\nRESULT: FAIL")
        return 1

    # --- Test 4: output JSON conforms to outputSchema ---
    structured = res.get("structuredContent")
    check("4. structuredContent returned", structured is not None)
    if structured is not None and has_schema:
        errs = conforms(structured, oschema)
        check("   output conforms to outputSchema", not errs,
              "" if not errs else f"{len(errs)} violation(s): {errs[:3]}")

    served = (structured or {}).get("lessons", [])

    # --- Test 1: deploy check — served data matches the canonical file ---
    with open(CANONICAL) as f:
        canonical = json.load(f)["lightningLessons"]

    check("1. deploy check: lesson count matches canonical file",
          len(served) == len(canonical), f"served={len(served)} file={len(canonical)}")

    by_id = {l["id"]: l for l in served}
    missing = [l["id"] for l in canonical if l["id"] not in by_id]
    check("   every canonical lesson is served", not missing,
          "" if not missing else f"missing: {missing}")

    drift = []
    for want in canonical:
        got = by_id.get(want["id"])
        if not got:
            continue
        for field in COMPARED_FIELDS:
            if want.get(field) != got.get(field):
                drift.append(f"{want['id']}.{field}")
    check("   served lessons match the file field-for-field", not drift,
          "" if not drift else f"{len(drift)} drifted: {drift[:5]}")

    failed = [n for n, ok, _ in results if not ok]
    print(f"\nRESULT: {'PASS' if not failed else 'FAIL'} — {len(results) - len(failed)}/{len(results)} checks passed")
    if failed:
        print("\nIf test 1 or 5 failed but the rest passed, the code is fine and the DEPLOY did not land.")
        print("Deploy is a manual change in Replit (Emmanuel) — pushing git does not deploy.")
        print(f"Test 5 failing means the live build predates the v{EXPECTED_VERSION} submitted to OpenAI.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
