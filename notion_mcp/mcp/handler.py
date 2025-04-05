"""MCP handler for the Notion API."""

from typing import Any, Dict, List, Optional, cast

import mcp.types as types
from mcp.server.lowlevel import Handler

from notion_mcp.api.client import NotionClient, SearchParams
from notion_mcp.mcp.models import (
    AppendBlocksRequest,
    Capability,
    CapabilityType,
    Category,
    CreatePageRequest,
    DeleteBlockRequest,
    GetBlockRequest,
    GetDatabaseRequest,
    GetPageRequest,
    ListBlocksRequest,
    NotionDataSource,
    Parameter,
    QueryDatabaseRequest,
    SearchRequest,
    UpdateBlockRequest,
    UpdatePageRequest,
)


def get_notion_capabilities() -> List[Capability]:
    """Get the capabilities for the Notion data source."""
    return [
        Capability(
            name="get_page",
            description="Get a Notion page by ID",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="page_id",
                    description="The ID of the page to get",
                    type="string",
                    required=True,
                ),
            ],
            category=Category.PAGE,
        ),
        Capability(
            name="update_page",
            description="Update a Notion page's properties",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="page_id",
                    description="The ID of the page to update",
                    type="string",
                    required=True,
                ),
                Parameter(
                    name="properties",
                    description="Properties to update",
                    type="object",
                    required=True,
                ),
            ],
            category=Category.PAGE,
        ),
        Capability(
            name="create_page",
            description="Create a new Notion page",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="parent",
                    description="Parent object (database_id or page_id)",
                    type="object",
                    required=True,
                ),
                Parameter(
                    name="properties",
                    description="Page properties",
                    type="object",
                    required=True,
                ),
                Parameter(
                    name="children",
                    description="Children blocks",
                    type="array",
                    required=False,
                ),
            ],
            category=Category.PAGE,
        ),
        Capability(
            name="get_database",
            description="Get a Notion database by ID",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="database_id",
                    description="The ID of the database to get",
                    type="string",
                    required=True,
                ),
            ],
            category=Category.DATABASE,
        ),
        Capability(
            name="query_database",
            description="Query a Notion database",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="database_id",
                    description="The ID of the database to query",
                    type="string",
                    required=True,
                ),
                Parameter(
                    name="filter",
                    description="Filter to apply to the database query",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="sorts",
                    description="Sort order for the database query",
                    type="array",
                    required=False,
                ),
                Parameter(
                    name="start_cursor",
                    description="Pagination cursor",
                    type="string",
                    required=False,
                ),
                Parameter(
                    name="page_size",
                    description="Number of results to return per page",
                    type="integer",
                    required=False,
                ),
            ],
            category=Category.DATABASE,
        ),
        Capability(
            name="get_block",
            description="Get a Notion block by ID",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="block_id",
                    description="The ID of the block to get",
                    type="string",
                    required=True,
                ),
            ],
            category=Category.BLOCK,
        ),
        Capability(
            name="update_block",
            description="Update a Notion block's content",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="block_id",
                    description="The ID of the block to update",
                    type="string",
                    required=True,
                ),
                Parameter(
                    name="content",
                    description="Content to update",
                    type="object",
                    required=True,
                ),
            ],
            category=Category.BLOCK,
        ),
        Capability(
            name="list_blocks",
            description="List a Notion block's children",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="block_id",
                    description="The ID of the block to list children for",
                    type="string",
                    required=True,
                ),
                Parameter(
                    name="start_cursor",
                    description="Pagination cursor",
                    type="string",
                    required=False,
                ),
                Parameter(
                    name="page_size",
                    description="Number of results to return per page",
                    type="integer",
                    required=False,
                ),
            ],
            category=Category.BLOCK,
        ),
        Capability(
            name="append_blocks",
            description="Append blocks to a Notion block's children",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="block_id",
                    description="The ID of the block to append children to",
                    type="string",
                    required=True,
                ),
                Parameter(
                    name="children",
                    description="Children blocks to append",
                    type="array",
                    required=True,
                ),
            ],
            category=Category.BLOCK,
        ),
        Capability(
            name="delete_block",
            description="Delete a Notion block",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="block_id",
                    description="The ID of the block to delete",
                    type="string",
                    required=True,
                ),
            ],
            category=Category.BLOCK,
        ),
        Capability(
            name="search",
            description="Search for Notion objects",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="query",
                    description="Search query",
                    type="string",
                    required=False,
                ),
                Parameter(
                    name="sort",
                    description="Sort order for search results",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="filter",
                    description="Filter to apply to search results",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="start_cursor",
                    description="Pagination cursor",
                    type="string",
                    required=False,
                ),
                Parameter(
                    name="page_size",
                    description="Number of results to return per page",
                    type="integer",
                    required=False,
                ),
            ],
            category=Category.SEARCH,
        ),
        Capability(
            name="create_database",
            description="Create a new Notion database",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="parent",
                    description="Parent object (page_id)",
                    type="object",
                    required=True,
                ),
                Parameter(
                    name="title",
                    description="Title of the database",
                    type="array",
                    required=True,
                ),
                Parameter(
                    name="properties",
                    description="Database properties schema",
                    type="object",
                    required=True,
                ),
                Parameter(
                    name="icon",
                    description="Icon object",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="cover",
                    description="Cover object",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="is_inline",
                    description="Whether the database is inline",
                    type="boolean",
                    required=False,
                ),
            ],
            category=Category.DATABASE,
        ),
        Capability(
            name="update_database",
            description="Update a Notion database",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="database_id",
                    description="The ID of the database to update",
                    type="string",
                    required=True,
                ),
                Parameter(
                    name="title",
                    description="Title of the database",
                    type="array",
                    required=False,
                ),
                Parameter(
                    name="properties",
                    description="Database properties schema",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="icon",
                    description="Icon object",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="cover",
                    description="Cover object",
                    type="object",
                    required=False,
                ),
                Parameter(
                    name="is_inline",
                    description="Whether the database is inline",
                    type="boolean",
                    required=False,
                ),
            ],
            category=Category.DATABASE,
        ),
        Capability(
            name="create_comment",
            description="Create a Notion comment",
            type=CapabilityType.OPERATION,
            parameters=[
                Parameter(
                    name="parent",
                    description="Parent object (page_id or block_id)",
                    type="object",
                    required=True,
                ),
                Parameter(
                    name="rich_text",
                    description="Rich text content of the comment",
                    type="array",
                    required=True,
                ),
                Parameter(
                    name="discussion_id",
                    description="ID of the discussion thread",
                    type="string",
                    required=False,
                ),
            ],
            category=Category.BLOCK,
        ),
        Capability(
            name="get_comment",
            description="Retrieve a Notion comment",
            type=CapabilityType.QUERY,
            parameters=[
                Parameter(
                    name="comment_id",
                    description="The ID of the comment to get",
                    type="string",
                    required=True,
                ),
            ],
            category=Category.BLOCK,
        ),
    ]


class NotionMCPHandler(mcp.types.MCPHandler):
    """MCP handler for the Notion API."""
    
    def __init__(self):
        """Initialize the handler."""
        super().__init__()
        self.notion_client = NotionClient()
        self.data_source = NotionDataSource(
            capabilities=get_notion_capabilities(),
        )
    
    def get_data_source_config(self) -> Dict[str, Any]:
        """Get the data source configuration."""
        return self.data_source.dict()
    
    def handle_query(
        self,
        capability_name: str,
        params: Dict[str, Any],
        context: Optional[mcp.types.MCPRequestContext] = None,
    ) -> Dict[str, Any]:
        """Handle a query capability.
        
        Args:
            capability_name: Capability name
            params: Parameters for the capability
            context: Request context
            
        Returns:
            Query response
        """
        client = NotionClient()
        
        if capability_name == "get_page":
            request = GetPageRequest(**params)
            return client.get_page(request.page_id).dict()
        
        elif capability_name == "get_database":
            request = GetDatabaseRequest(**params)
            return client.get_database(request.database_id).dict()
        
        elif capability_name == "query_database":
            request = QueryDatabaseRequest(**params)
            return client.query_database(
                database_id=request.database_id,
                filter=request.filter,
                sorts=request.sorts,
                start_cursor=request.start_cursor,
                page_size=request.page_size,
            )
        
        elif capability_name == "get_block":
            request = GetBlockRequest(**params)
            return client.get_block(request.block_id).dict()
        
        elif capability_name == "list_blocks":
            request = ListBlocksRequest(**params)
            from notion_mcp.api.client import ListBlocksParams
            
            list_params = None
            if request.start_cursor or request.page_size:
                list_params = ListBlocksParams(
                    start_cursor=request.start_cursor,
                    page_size=request.page_size,
                )
            
            return client.list_blocks(
                block_id=request.block_id,
                params=list_params,
            )
        
        elif capability_name == "search":
            request = SearchRequest(**params)
            from notion_mcp.api.client import SearchParams
            
            search_params = SearchParams(
                query=request.query,
                sort=request.sort,
                filter=request.filter,
                start_cursor=request.start_cursor,
                page_size=request.page_size,
            )
            
            return client.search(search_params)
        
        elif capability_name == "get_comment":
            request = GetCommentRequest(**params)
            return client.get_comment(request.comment_id)
        
        else:
            raise ValueError(f"Unknown query capability: {capability_name}")
    
    def handle_operation(
        self,
        capability_name: str,
        params: Dict[str, Any],
        context: Optional[mcp.types.MCPRequestContext] = None,
    ) -> Dict[str, Any]:
        """Handle an operation capability.
        
        Args:
            capability_name: Capability name
            params: Parameters for the capability
            context: Request context
            
        Returns:
            Operation response
        """
        client = NotionClient()
        
        if capability_name == "create_page":
            request = CreatePageRequest(**params)
            return client.create_page(
                parent=request.parent,
                properties=request.properties,
                children=request.children,
            ).dict()
        
        elif capability_name == "update_page":
            request = UpdatePageRequest(**params)
            return client.update_page(
                page_id=request.page_id,
                properties=request.properties,
            ).dict()
        
        elif capability_name == "update_block":
            request = UpdateBlockRequest(**params)
            return client.update_block(
                block_id=request.block_id,
                content=request.content,
            ).dict()
        
        elif capability_name == "append_blocks":
            request = AppendBlocksRequest(**params)
            return client.append_blocks(
                block_id=request.block_id,
                children=request.children,
            )
        
        elif capability_name == "delete_block":
            request = DeleteBlockRequest(**params)
            return client.delete_block(request.block_id).dict()

        elif capability_name == "create_database":
            request = CreateDatabaseRequest(**params)
            return client.create_database(
                parent=request.parent,
                title=request.title,
                properties=request.properties,
                icon=request.icon,
                cover=request.cover,
                is_inline=request.is_inline,
            ).dict()
        
        elif capability_name == "update_database":
            request = UpdateDatabaseRequest(**params)
            return client.update_database(
                database_id=request.database_id,
                title=request.title,
                properties=request.properties,
                icon=request.icon,
                cover=request.cover,
                is_inline=request.is_inline,
            ).dict()
        
        elif capability_name == "create_comment":
            request = CreateCommentRequest(**params)
            return client.create_comment(
                parent=request.parent,
                rich_text=request.rich_text,
                discussion_id=request.discussion_id,
            )
        
        else:
            raise ValueError(f"Unknown operation capability: {capability_name}")
    
    def handle_contextual_operation(
        self,
        capability_name: str,
        params: Dict[str, Any],
        context: Optional[mcp.types.MCPRequestContext] = None,
    ) -> Dict[str, Any]:
        """Handle a contextual operation capability.
        
        Args:
            capability_name: The name of the capability to invoke
            params: The parameters for the capability
            context: Request context
            
        Returns:
            The result of the contextual operation
        """
        # Not implemented for Notion
        raise ValueError(f"Unknown contextual operation capability: {capability_name}") 