# Notion MCP Server Implementation

This document describes the implementation of the Notion MCP server.

## Project Structure

```
notion-mcp/
├── LICENSE               # Apache License 2.0
├── README.md             # Project README
├── docs/                 # Documentation
├── examples/             # Example scripts
├── notion_mcp/           # Main package
│   ├── __init__.py
│   ├── api/              # Notion API client
│   │   ├── __init__.py
│   │   └── client.py
│   ├── config/           # Configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── mcp/              # MCP implementation
│   │   ├── __init__.py
│   │   ├── handler.py
│   │   └── models.py
│   ├── models/           # Data models
│   │   ├── __init__.py
│   │   └── notion.py
│   ├── server.py         # Server implementation
│   └── utils/            # Utilities
│       ├── __init__.py
│       └── notion.py
├── pyproject.toml        # Project metadata
└── requirements-dev.txt  # Development dependencies
```

## Implementation Details

### MCP Protocol

The Model Context Protocol (MCP) is a standard for AI models to interact with external systems. The Notion MCP server implements this protocol to enable AI models to interact with Notion using the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).

The MCP protocol allows tools to be exposed to LLMs (like Claude) through a standardized interface. The Notion MCP server exposes Notion's API as a set of tools that can be called by LLMs.

### Transport Methods

The Notion MCP server supports two transport methods:

1. **Standard Input/Output (stdio)**: This is the default mode and is used by Claude for Desktop and other LLM clients that support launching tools as subprocesses.

2. **Server-Sent Events (SSE)**: This transport allows web-based clients to communicate with the MCP server over HTTP.

### Tools

The server implements the following tools that map to Notion API operations:

#### Page Operations
- `get_page`: Get a Notion page by ID
- `update_page`: Update a Notion page's properties
- `create_page`: Create a new Notion page

#### Database Operations
- `get_database`: Get a Notion database by ID
- `query_database`: Query a Notion database

#### Block Operations
- `get_block`: Get a Notion block by ID
- `update_block`: Update a Notion block's content
- `list_blocks`: List a block's children
- `append_blocks`: Append blocks to a block's children
- `delete_block`: Delete a Notion block

#### Search Operations
- `search`: Search for Notion objects

Each tool is defined with an input schema that specifies the required and optional parameters.

### Notion API Client

The Notion API client (`notion_mcp/api/client.py`) handles the interaction with Notion's API. It provides methods for all the supported operations and handles error handling and response parsing.

### MCP Server Implementation

The MCP server implementation (`notion_mcp/server.py`) creates an MCP server using the low-level API from the MCP Python SDK:

```python
app = Server("notion-mcp")

@app.list_tools()
async def list_tools() -> List[types.Tool]:
    # Return a list of available tools
    ...

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.Content]:
    # Handle tool calls and dispatch to Notion API
    ...
```

The server handles tool calls by:
1. Receiving the tool name and arguments
2. Dispatching to the appropriate Notion API client method
3. Converting the result to a text response in the MCP format

## Using the Notion MCP Server

### Prerequisites

1. Python 3.12 or higher
2. A Notion integration with an API key

### Configuration

Set your Notion API key as an environment variable:

```bash
export NOTION_API_KEY="your_api_key_here"
```

### Running the Server

For stdio transport (default for Claude for Desktop):
```bash
python -m notion_mcp.server
```

For SSE transport (for web clients):
```bash
python -m notion_mcp.server --transport sse --host 0.0.0.0 --port 8000
```

## Example Client

The repository includes an example client (`examples/client_example.py`) that demonstrates how to call the MCP server programmatically using both stdio and SSE transports.

### Using with Claude for Desktop

To use this MCP server with Claude for Desktop:

1. Start the server in stdio mode: `python -m notion_mcp.server`
2. In Claude for Desktop, add a new tool
3. Follow the prompts to select "Add a server using stdio"
4. Choose the appropriate executable based on your environment
5. Provide a name and description for the tool

## Extending the Server

To add a new capability:

1. Add the new tool to the `list_tools()` method in `notion_mcp/server.py`
2. Add a new handler for the tool in the `call_tool()` method
3. Add the corresponding method to the `NotionClient` class if needed 