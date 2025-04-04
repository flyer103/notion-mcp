"""Server module to run the MCP server."""

import argparse
import asyncio
import logging
import os
from typing import Any, Dict, List, Optional, cast

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server

from notion_mcp.api.client import NotionClient, SearchParams
from notion_mcp.config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_server() -> Server:
    """Create an MCP server for Notion.
    
    Returns:
        MCP server instance
    """
    app = Server("notion-mcp")
    
    # Create Notion client
    notion_client = NotionClient()
    
    # Register capabilities as tools
    
    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        """List available tools."""
        tools = []
        
        # Page tools
        tools.append(
            types.Tool(
                name="get_page",
                description="Get a Notion page by ID",
                inputSchema={
                    "type": "object",
                    "required": ["page_id"],
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page to get",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="update_page",
                description="Update a Notion page's properties",
                inputSchema={
                    "type": "object",
                    "required": ["page_id", "properties"],
                    "properties": {
                        "page_id": {
                            "type": "string",
                            "description": "The ID of the page to update",
                        },
                        "properties": {
                            "type": "object",
                            "description": "Properties to update",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="create_page",
                description="Create a new Notion page",
                inputSchema={
                    "type": "object",
                    "required": ["parent", "properties"],
                    "properties": {
                        "parent": {
                            "type": "object",
                            "description": "Parent object (database_id or page_id)",
                        },
                        "properties": {
                            "type": "object",
                            "description": "Page properties",
                        },
                        "children": {
                            "type": "array",
                            "description": "Children blocks",
                        }
                    },
                },
            )
        )
        
        # Database tools
        tools.append(
            types.Tool(
                name="get_database",
                description="Get a Notion database by ID",
                inputSchema={
                    "type": "object",
                    "required": ["database_id"],
                    "properties": {
                        "database_id": {
                            "type": "string",
                            "description": "The ID of the database to get",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="query_database",
                description="Query a Notion database",
                inputSchema={
                    "type": "object",
                    "required": ["database_id"],
                    "properties": {
                        "database_id": {
                            "type": "string",
                            "description": "The ID of the database to query",
                        },
                        "filter": {
                            "type": "object",
                            "description": "Filter to apply to the database query",
                        },
                        "sorts": {
                            "type": "array",
                            "description": "Sort order for the database query",
                        },
                        "start_cursor": {
                            "type": "string",
                            "description": "Pagination cursor",
                        },
                        "page_size": {
                            "type": "integer",
                            "description": "Number of results to return per page",
                        }
                    },
                },
            )
        )
        
        # Block tools
        tools.append(
            types.Tool(
                name="get_block",
                description="Get a Notion block by ID",
                inputSchema={
                    "type": "object",
                    "required": ["block_id"],
                    "properties": {
                        "block_id": {
                            "type": "string",
                            "description": "The ID of the block to get",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="update_block",
                description="Update a Notion block's content",
                inputSchema={
                    "type": "object",
                    "required": ["block_id", "content"],
                    "properties": {
                        "block_id": {
                            "type": "string",
                            "description": "The ID of the block to update",
                        },
                        "content": {
                            "type": "object",
                            "description": "Content to update",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="list_blocks",
                description="List a Notion block's children",
                inputSchema={
                    "type": "object",
                    "required": ["block_id"],
                    "properties": {
                        "block_id": {
                            "type": "string",
                            "description": "The ID of the block to list children for",
                        },
                        "start_cursor": {
                            "type": "string",
                            "description": "Pagination cursor",
                        },
                        "page_size": {
                            "type": "integer",
                            "description": "Number of results to return per page",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="append_blocks",
                description="Append blocks to a Notion block's children",
                inputSchema={
                    "type": "object",
                    "required": ["block_id", "children"],
                    "properties": {
                        "block_id": {
                            "type": "string",
                            "description": "The ID of the block to append children to",
                        },
                        "children": {
                            "type": "array",
                            "description": "Children blocks to append",
                        }
                    },
                },
            )
        )
        
        tools.append(
            types.Tool(
                name="delete_block",
                description="Delete a Notion block",
                inputSchema={
                    "type": "object",
                    "required": ["block_id"],
                    "properties": {
                        "block_id": {
                            "type": "string",
                            "description": "The ID of the block to delete",
                        }
                    },
                },
            )
        )
        
        # Search tools
        tools.append(
            types.Tool(
                name="search",
                description="Search for Notion objects",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query",
                        },
                        "sort": {
                            "type": "object",
                            "description": "Sort order for search results",
                        },
                        "filter": {
                            "type": "object",
                            "description": "Filter to apply to search results",
                        },
                        "start_cursor": {
                            "type": "string",
                            "description": "Pagination cursor",
                        },
                        "page_size": {
                            "type": "integer",
                            "description": "Number of results to return per page",
                        }
                    },
                },
            )
        )
        
        return tools
    
    @app.call_tool()
    async def call_tool(
        name: str, arguments: Dict[str, Any]
    ) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool calls."""
        try:
            result: Any = None
            
            # Dispatch to the appropriate Notion API method
            if name == "get_page":
                result = notion_client.get_page(arguments["page_id"])
            
            elif name == "update_page":
                result = notion_client.update_page(
                    page_id=arguments["page_id"],
                    properties=arguments["properties"],
                )
            
            elif name == "create_page":
                children = arguments.get("children")
                result = notion_client.create_page(
                    parent=arguments["parent"],
                    properties=arguments["properties"],
                    children=children,
                )
            
            elif name == "get_database":
                result = notion_client.get_database(arguments["database_id"])
            
            elif name == "query_database":
                filter_arg = arguments.get("filter")
                sorts = arguments.get("sorts")
                start_cursor = arguments.get("start_cursor")
                page_size = arguments.get("page_size")
                
                result = notion_client.query_database(
                    database_id=arguments["database_id"],
                    filter=filter_arg,
                    sorts=sorts,
                    start_cursor=start_cursor,
                    page_size=page_size,
                )
            
            elif name == "get_block":
                result = notion_client.get_block(arguments["block_id"])
            
            elif name == "update_block":
                result = notion_client.update_block(
                    block_id=arguments["block_id"],
                    content=arguments["content"],
                )
            
            elif name == "list_blocks":
                from notion_mcp.api.client import ListBlocksParams
                
                params = None
                if "start_cursor" in arguments or "page_size" in arguments:
                    params = ListBlocksParams(
                        start_cursor=arguments.get("start_cursor"),
                        page_size=arguments.get("page_size"),
                    )
                
                result = notion_client.list_blocks(
                    block_id=arguments["block_id"],
                    params=params,
                )
            
            elif name == "append_blocks":
                result = notion_client.append_blocks(
                    block_id=arguments["block_id"],
                    children=arguments["children"],
                )
            
            elif name == "delete_block":
                result = notion_client.delete_block(arguments["block_id"])
            
            elif name == "search":
                from notion_mcp.api.client import SearchParams
                
                params = SearchParams(
                    query=arguments.get("query"),
                    sort=arguments.get("sort"),
                    filter=arguments.get("filter"),
                    start_cursor=arguments.get("start_cursor"),
                    page_size=arguments.get("page_size"),
                )
                
                result = notion_client.search(params)
            
            else:
                raise ValueError(f"Unknown tool: {name}")
            
            # Convert result to text for the response
            if hasattr(result, "dict"):
                # Pydantic model
                result_text = str(result.dict())
            else:
                # Dictionary or other JSON-serializable object
                result_text = str(result)
            
            return [types.TextContent(type="text", text=result_text)]
        
        except Exception as e:
            logger.exception(f"Error handling tool call {name}")
            return [types.TextContent(
                type="text", 
                text=f"Error calling {name}: {str(e)}"
            )]
    
    return app


def main():
    """Run the MCP server."""
    parser = argparse.ArgumentParser(description="Notion MCP Server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=settings.server.port,
        help="Port to listen on for SSE transport"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default=settings.server.host,
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport type (stdio or sse)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    # Set debug mode if specified
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create the MCP server
    app = create_server()
    
    # Run with the selected transport
    if args.transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        
        sse = SseServerTransport("/messages/")
        
        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
        
        starlette_app = Starlette(
            debug=args.debug,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )
        
        import uvicorn
        
        logger.info(f"Starting Notion MCP Server with SSE transport on {args.host}:{args.port}")
        uvicorn.run(starlette_app, host=args.host, port=args.port)
    else:
        from mcp.server.stdio import stdio_server
        
        logger.info("Starting Notion MCP Server with stdio transport")
        
        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
        
        anyio.run(arun)


if __name__ == "__main__":
    main() 