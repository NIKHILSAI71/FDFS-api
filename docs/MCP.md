# FDFS MCP Integration

## Overview

FDFS (First Day First Show) provides an MCP (Model Context Protocol) server for integrating movie data with AI assistants like Claude.

## Setup

### 1. Install Dependencies
```bash
pip install mcp
```

### 2. Run MCP Server
```bash
python -m mcp.mcp_server
```

### 3. Configure Claude Desktop

Add to your Claude config (`~/.config/claude/config.json`):

```json
{
  "mcpServers": {
    "fdfs": {
      "command": "python",
      "args": ["-m", "mcp.mcp_server"],
      "cwd": "/path/to/FDFS-API"
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_regions` | List all cities |
| `search_movies` | Search movies by name |
| `get_theaters` | List theaters in a region |
| `get_now_showing` | Currently showing movies |

## Example Prompts

- "What movies are showing in Hyderabad?"
- "Search for Pushpa 2"
- "List theaters in Mumbai"
