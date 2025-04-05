# Notion MCP Server

A Model Context Protocol (MCP) server for interacting with Notion APIs.

## Overview

This project implements an MCP server that interfaces with Notion's API, allowing AI models to interact with Notion documents and data. It follows the [Model Context Protocol](https://modelcontextprotocol.io/) specification and uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).

## Requirements

- Python 3.12 or higher
- `uv` for package management

## Installation

```bash
# Clone the repository
git clone https://github.com/flyer103/notion-mcp.git
cd notion-mcp

# Install dependencies using uv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Configuration

Before using the Notion MCP server, you need to set up a Notion integration and get an API key:

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Set the API key as an environment variable:

```bash
export NOTION_API_KEY="your_api_key_here"
```

4. Share your Notion content with the integration:
   - Open the Notion page you want to access
   - Click the "..." menu in the top-right corner
   - Select "Add connections"
   - Find and select your integration from the list
   - The integration now has access to this page and all its subpages

## Usage

The Notion MCP server supports two transport methods:

### 1. Standard Input/Output (stdio)

This is the default mode, used by Claude for Desktop and other MCP-compatible LLM clients:

```bash
python -m notion_mcp.server
```

### 2. Server-Sent Events (SSE)

For web-based integrations, you can use the SSE transport:

```bash
python -m notion_mcp.server --transport sse --host 0.0.0.0 --port 8000
```

The server will be available at http://localhost:8000/sse

## Available Tools

The Notion MCP server provides the following capabilities as tools:

### Page Operations
- `get_page`: Get a Notion page by ID
- `update_page`: Update a Notion page's properties
- `create_page`: Create a new Notion page

### Database Operations
- `get_database`: Get a Notion database by ID
- `query_database`: Query a Notion database

### Block Operations
- `get_block`: Get a Notion block by ID
- `update_block`: Update a Notion block's content
- `list_blocks`: List a block's children
- `append_blocks`: Append blocks to a block's children
- `delete_block`: Delete a Notion block

### Search Operations
- `search`: Search for Notion objects

## Command-Line Options

```
usage: python -m notion_mcp.server [-h] [--port PORT] [--host HOST] [--transport {stdio,sse}] [--debug]

Notion MCP Server

options:
  -h, --help            show this help message and exit
  --port PORT           Port to listen on for SSE transport
  --host HOST           Host to bind the server to
  --transport {stdio,sse}
                        Transport type (stdio or sse)
  --debug               Enable debug mode
```

## Testing with Claude for Desktop

To use this MCP server with Claude for Desktop, you need to create a configuration file:

1. Create a file called `claude_desktop_config.json` (not claude-for-desktop-tools.json) in the following location:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the following configuration to the file (adjust paths as needed):

```json
{
  "mcpServers": {
    "notion-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/YOUR/notion-mcp",
        "run",
        "-m",
        "notion_mcp.server"
      ],
      "env": {
        "NOTION_API_KEY": "your_notion_api_key"
      }
    }
  }
}
```

3. Replace `/ABSOLUTE/PATH/TO/YOUR/notion-mcp` with the absolute path to your notion-mcp installation
4. Replace `your_notion_api_key` with your Notion API key (or you can omit the env section if you've set it as a system environment variable)
5. Save the file and restart Claude for Desktop

You can check Claude's logs for any MCP-related issues:
```bash
# Check Claude's logs for errors
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
```

Claude will now have access to your Notion MCP server and can interact with Notion documents. You can ask Claude to perform actions like "Create a page in Notion" or "Search my Notion workspace."

### Verifying Configuration

To verify that Claude is correctly configured to use your Notion MCP server, you can ask Claude:
"Can you list the tools you have access to?" or "Can you create a new page in my Notion workspace?"

If there are any connection issues, check that:
- The configuration file is correctly formatted and in the right location
- The paths in the configuration are correct
- Your Notion integration has the proper permissions

### Troubleshooting Common Issues

#### "spawn uv ENOENT" Error

If you encounter this error:
```
spawn uv ENOENT {"context":"connection","stack":"Error: spawn uv ENOENT\n at ChildProcess._handle.onexit (node:internal/child_process:285:19)\n at onErrorNT (node:internal/child_process:483:16)\n at process.processTicksAndRejections (node:internal/process/task_queues:82:21)"}
```

This means Claude Desktop cannot find the `uv` executable in your PATH. To fix this:

1. Find the absolute path to your `uv` executable:
   ```bash
   # On macOS/Linux
   which uv

   # On Windows
   where uv
   ```

2. Use the full absolute path in your configuration:
   ```json
   {
     "mcpServers": {
       "notion-mcp": {
         "command": "/ABSOLUTE/PATH/TO/YOUR/uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/YOUR/notion-mcp",
           "run",
           "-m",
           "notion_mcp.server"
         ],
         "env": {
           "NOTION_API_KEY": "your_notion_api_key"
         }
       }
     }
   }
   ```

3. Save the file and restart Claude Desktop.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details. 