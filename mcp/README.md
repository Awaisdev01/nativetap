# nativetap MCP server

Expose the 461 mobile design rules as MCP tools — works in Claude Code,
Cursor, Codex, Windsurf, and any MCP client. Zero dependencies (Python 3 stdlib only).

## Tools

| Tool | What it does |
|---|---|
| `search_mobile_rules` | Search all 42 domains; optional `domain` or `stack` filter |
| `list_domains` | List the 42 data domains |
| `thumb_rules` | The 40 prioritized thumb rules (P0–P5) |

## Install

Add to your MCP client config (e.g. `.mcp.json` / `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "nativetap": {
      "command": "python3",
      "args": ["/absolute/path/to/nativetap/mcp/server.py"]
    }
  }
}
```

The server reads the skill data from `../.claude/skills/nativetap/data/`
relative to its own location — keep the repo layout intact.

## Test

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 mcp/server.py
```
