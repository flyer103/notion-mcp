#!/usr/bin/env python3
"""Example client for the Notion MCP server."""

import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

import httpx

# Configuration
NOTION_PAGE_ID = os.environ.get("NOTION_PAGE_ID", "")  # Replace with your page ID


def call_stdio_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call a tool via stdio MCP.
    
    Args:
        tool_name: The name of the tool to invoke
        arguments: The arguments for the tool
        
    Returns:
        The result from the tool
    """
    # Create a subprocess for the MCP server
    proc = subprocess.Popen(
        [sys.executable, "-m", "notion_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    # Prepare the MCP request message
    request = {
        "type": "initialization",
        "body": {},
    }
    
    # Send the initialization request
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    
    # Read the response (should be initialization_response)
    initialization_response = json.loads(proc.stdout.readline())
    print(f"Initialization response: {initialization_response}\n")
    
    # Send the tool call
    tool_call_request = {
        "type": "message",
        "body": {
            "type": "tool_call",
            "name": tool_name,
            "arguments": arguments,
        },
    }
    
    proc.stdin.write(json.dumps(tool_call_request) + "\n")
    proc.stdin.flush()
    
    # Read the response
    tool_call_response = json.loads(proc.stdout.readline())
    
    # Close the subprocess
    proc.stdin.close()
    proc.terminate()
    proc.wait()
    
    # Return the response content
    if tool_call_response.get("type") == "message" and tool_call_response.get("body", {}).get("type") == "tool_call_response":
        contents = tool_call_response["body"].get("contents", [])
        if contents and contents[0].get("type") == "text":
            try:
                return json.loads(contents[0].get("text", "{}"))
            except json.JSONDecodeError:
                return {"result": contents[0].get("text")}
    
    return {"error": "Unexpected response format"}


def call_sse_mcp_tool(
    tool_name: str, 
    arguments: Dict[str, Any], 
    base_url: str = "http://localhost:8000"
) -> Dict[str, Any]:
    """Call a tool via SSE MCP.
    
    Args:
        tool_name: The name of the tool to invoke
        arguments: The arguments for the tool
        base_url: The base URL of the MCP server
        
    Returns:
        The result from the tool
    """
    sse_url = f"{base_url}/sse"
    message_url = f"{base_url}/messages/"
    
    # Establish the SSE connection
    with httpx.Client() as client:
        # Send the initialization message
        init_request = {
            "type": "initialization",
            "body": {},
        }
        
        init_response = client.post(
            message_url,
            json=init_request,
        )
        init_response.raise_for_status()
        
        # Send the tool call message
        tool_call_request = {
            "type": "message",
            "body": {
                "type": "tool_call",
                "name": tool_name,
                "arguments": arguments,
            },
        }
        
        tool_call_response = client.post(
            message_url,
            json=tool_call_request,
        )
        tool_call_response.raise_for_status()
        
        # Process the response
        if tool_call_response.status_code == 200:
            response_json = tool_call_response.json()
            if response_json.get("type") == "message" and response_json.get("body", {}).get("type") == "tool_call_response":
                contents = response_json["body"].get("contents", [])
                if contents and contents[0].get("type") == "text":
                    try:
                        return json.loads(contents[0].get("text", "{}"))
                    except json.JSONDecodeError:
                        return {"result": contents[0].get("text")}
        
        return {"error": "Failed to get a valid response"}


def example_get_page(use_sse: bool = False) -> Dict[str, Any]:
    """Example of getting a page from Notion.
    
    Args:
        use_sse: Whether to use SSE transport
    
    Returns:
        The page data
    """
    if not NOTION_PAGE_ID:
        raise ValueError("NOTION_PAGE_ID environment variable is required")
    
    arguments = {"page_id": NOTION_PAGE_ID}
    
    if use_sse:
        return call_sse_mcp_tool("get_page", arguments)
    else:
        return call_stdio_mcp_tool("get_page", arguments)


def example_search(use_sse: bool = False) -> Dict[str, Any]:
    """Example of searching for objects in Notion.
    
    Args:
        use_sse: Whether to use SSE transport
    
    Returns:
        The search results
    """
    arguments = {"query": "example"}
    
    if use_sse:
        return call_sse_mcp_tool("search", arguments)
    else:
        return call_stdio_mcp_tool("search", arguments)


def example_create_page(use_sse: bool = False) -> Dict[str, Any]:
    """Example of creating a page in Notion.
    
    Args:
        use_sse: Whether to use SSE transport
    
    Returns:
        The created page data
    """
    if not NOTION_PAGE_ID:
        raise ValueError("NOTION_PAGE_ID environment variable is required")
    
    arguments = {
        "parent": {"page_id": NOTION_PAGE_ID},
        "properties": {
            "title": {"title": [{"text": {"content": "Example Page"}}]},
        },
        "children": [
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "This is an example page created via MCP."}}
                    ],
                },
            },
            {
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {"text": {"content": "Heading 1"}}
                    ],
                },
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"text": {"content": "Bullet point 1"}}
                    ],
                },
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"text": {"content": "Bullet point 2"}}
                    ],
                },
            },
        ],
    }
    
    if use_sse:
        return call_sse_mcp_tool("create_page", arguments)
    else:
        return call_stdio_mcp_tool("create_page", arguments)


def example_append_blocks(block_id: str, use_sse: bool = False) -> Dict[str, Any]:
    """Example of appending blocks to a block in Notion.
    
    Args:
        block_id: The ID of the block to append to
        use_sse: Whether to use SSE transport
        
    Returns:
        The updated block data
    """
    arguments = {
        "block_id": block_id,
        "children": [
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"text": {"content": "This is an appended paragraph."}}
                    ],
                },
            },
        ],
    }
    
    if use_sse:
        return call_sse_mcp_tool("append_blocks", arguments)
    else:
        return call_stdio_mcp_tool("append_blocks", arguments)


def main():
    """Run the example."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Notion MCP Client Example')
    parser.add_argument('--sse', action='store_true', help='Use SSE transport')
    args = parser.parse_args()
    
    # Get a page
    print("Getting a page...")
    try:
        page_data = example_get_page(args.sse)
        print(f"Page ID: {page_data.get('id', 'Unknown')}")
    except Exception as e:
        print(f"Error getting page: {e}")
    
    # Search for objects
    print("\nSearching for objects...")
    try:
        search_results = example_search(args.sse)
        result_count = len(search_results.get("results", []))
        print(f"Found {result_count} objects")
    except Exception as e:
        print(f"Error searching: {e}")
    
    # Create a page
    print("\nCreating a page...")
    try:
        new_page = example_create_page(args.sse)
        new_page_id = new_page.get("id")
        print(f"Created page with ID: {new_page_id}")
        
        # Append blocks to the page
        if new_page_id:
            print("\nAppending blocks to the page...")
            updated_blocks = example_append_blocks(new_page_id, args.sse)
            print(f"Updated blocks: {len(updated_blocks.get('results', []))} blocks")
    except Exception as e:
        print(f"Error creating page: {e}")
    
    print("\nDone!")


if __name__ == "__main__":
    main() 