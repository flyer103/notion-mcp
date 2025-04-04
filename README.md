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

To use this MCP server with Claude for Desktop:

1. Start the server in stdio mode: `python -m notion_mcp.server`
2. In Claude for Desktop, add a new tool
3. Follow the prompts to select "Add a server using stdio"
4. Choose the appropriate executable based on your environment
5. Provide a name and description for the tool

Claude can now use your Notion MCP server to interact with Notion documents.

## Example Client

For an example of how to call the MCP server programmatically, see the `examples/client_example.py` file.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details. 