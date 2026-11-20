#!/usr/bin/env python3
"""nativetap MCP server — exposes the mobile design rulebook as MCP tools.

Stdio JSON-RPC 2.0, zero dependencies. Install in any MCP client:
  {"mcpServers": {"nativetap": {"command": "python3",
   "args": ["/path/to/nativetap/mcp/server.py"]}}}
"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SEARCH = os.path.join(BASE, '..', '.claude', 'skills', 'nativetap', 'scripts', 'search.py')

TOOLS = [
    {
        "name": "search_mobile_rules",
        "description": ("Search 461 curated mobile UI/UX rules across 42 domains: "
                        "Apple HIG, Material 3, Flutter, SwiftUI, Jetpack Compose "
                        "patterns, gestures + haptics, safe areas, dark mode, motion, "
                        "a11y, performance, store assets. Use before writing any "
                        "mobile UI."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "e.g. 'keyboard covers field', 'touch target', 'dark mode'"},
                "domain": {"type": "string", "description": "optional: restrict to one domain, e.g. flutter, hig-ios, gestures"},
                "stack": {"type": "string", "enum": ["flutter", "swiftui", "kotlin", "design", "launch"], "description": "optional: route to domains relevant to this stack"},
                "max_results": {"type": "integer", "default": 3},
            },
            "required": ["query"],
        },
    },
    {
        "name": "list_domains",
        "description": "List all 42 nativetap data domains.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "thumb_rules",
        "description": "Print the 40 thumb rules (P0-P5 prioritized mobile non-negotiables).",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def call_search(args):
    cmd = [sys.executable, SEARCH]
    if not os.path.exists(SEARCH):
        return [{"type": "text", "text": "nativetap data not found — install the repo first"}]
    if args.get('domain'):
        cmd += ['--domain', args['domain']]
    if args.get('stack'):
        cmd += ['--stack', args['stack']]
    cmd += ['--json', args.get('query', ''), '--max-results', str(args.get('max_results', 3))]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        rows = json.loads(out.stdout) if out.stdout.strip() else []
        if not rows:
            return [{"type": "text", "text": f"No matches for '{args.get('query')}'."}]
        text = json.dumps(rows, indent=1, ensure_ascii=False)
        return [{"type": "text", "text": text[:12000]}]
    except Exception as e:
        return [{"type": "text", "text": f"search error: {e}"}]


def call_list_domains(args):
    out = subprocess.run([sys.executable, SEARCH, '--list-domains', '--json'],
                         capture_output=True, text=True, timeout=10)
    return [{"type": "text", "text": ', '.join(json.loads(out.stdout))}]


def call_thumb_rules(args):
    out = subprocess.run([sys.executable, SEARCH, '--checklist'],
                         capture_output=True, text=True, timeout=10)
    return [{"type": "text", "text": out.stdout[:15000]}]


HANDLERS = {'search_mobile_rules': call_search,
            'list_domains': call_list_domains,
            'thumb_rules': call_thumb_rules}


def read_messages():
    buffer = ''
    for line in sys.stdin:
        buffer += line
        if '\n' in buffer or buffer.strip():
            try:
                yield json.loads(buffer)
                buffer = ''
            except json.JSONDecodeError:
                continue


def main():
    for msg in read_messages():
        method = msg.get('method', '')
        mid = msg.get('id')
        if method == 'initialize':
            result = {"protocolVersion": "2024-11-05",
                      "capabilities": {"tools": {}},
                      "serverInfo": {"name": "nativetap",
                                     "version": "1.0.0"}}
        elif method == 'notifications/initialized':
            continue
        elif method == 'tools/list':
            result = {"tools": TOOLS}
        elif method == 'tools/call':
            name = msg['params']['name']
            handler = HANDLERS.get(name)
            if handler:
                result = {"content": handler(msg['params'].get('arguments', {}))}
            else:
                result = {"content": [{"type": "text", "text": f"unknown tool {name}"}],
                          "isError": True}
        elif method == 'ping':
            result = {}
        else:
            if mid is None:
                continue
            result = None
            send({"jsonrpc": "2.0", "id": mid,
                  "error": {"code": -32601, "message": "method not found"}})
            continue
        if mid is not None:
            send({"jsonrpc": "2.0", "id": mid, "result": result})


def send(obj):
    sys.stdout.write(json.dumps(obj) + '\n')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
