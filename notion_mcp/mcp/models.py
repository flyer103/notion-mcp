"""Models for the MCP server."""

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class CapabilityType(str, Enum):
    """Type of capability in the MCP protocol."""
    
    QUERY = "query"
    OPERATION = "operation"
    CONTEXTUAL_OPERATION = "contextual_operation"


class Category(str, Enum):
    """Categories of operations in Notion."""
    
    PAGE = "page"
    DATABASE = "database"
    BLOCK = "block"
    SEARCH = "search"


class DataSourceType(str, Enum):
    """Types of data sources in the MCP protocol."""
    
    NOTION = "notion"


class ResourceType(str, Enum):
    """Types of resources in Notion."""
    
    PAGE = "page"
    DATABASE = "database"
    BLOCK = "block"


class Parameter(BaseModel):
    """Parameter for a capability."""
    
    name: str
    description: str
    type: str
    required: bool = False


class Capability(BaseModel):
    """Capability in the MCP protocol."""
    
    name: str
    description: str
    type: CapabilityType
    parameters: List[Parameter] = Field(default_factory=list)
    return_type: str = "object"
    category: Optional[Category] = None


class NotionDataSource(BaseModel):
    """Notion data source in the MCP protocol."""
    
    type: DataSourceType = DataSourceType.NOTION
    capabilities: List[Capability] = Field(default_factory=list)
    name: str = "Notion"
    description: str = "Interact with Notion pages, databases, and blocks."


class GetPageRequest(BaseModel):
    """Request to get a page."""
    
    page_id: str = Field(..., description="The ID of the page to get")


class GetDatabaseRequest(BaseModel):
    """Request to get a database."""
    
    database_id: str = Field(..., description="The ID of the database to get")


class QueryDatabaseRequest(BaseModel):
    """Request to query a database."""
    
    database_id: str = Field(..., description="The ID of the database to query")
    filter: Optional[Dict[str, Any]] = Field(
        None,
        description="Filter to apply to the database query",
    )
    sorts: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Sort order for the database query",
    )
    start_cursor: Optional[str] = Field(
        None,
        description="Pagination cursor",
    )
    page_size: Optional[int] = Field(
        None,
        description="Number of results to return per page",
    )


class GetBlockRequest(BaseModel):
    """Request to get a block."""
    
    block_id: str = Field(..., description="The ID of the block to get")


class CreatePageRequest(BaseModel):
    """Request to create a page."""
    
    parent: Dict[str, Any] = Field(
        ...,
        description="Parent object (database_id or page_id)",
    )
    properties: Dict[str, Any] = Field(
        ...,
        description="Page properties",
    )
    children: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Children blocks",
    )


class UpdatePageRequest(BaseModel):
    """Request to update a page."""
    
    page_id: str = Field(..., description="The ID of the page to update")
    properties: Dict[str, Any] = Field(
        ...,
        description="Page properties to update",
    )


class SearchRequest(BaseModel):
    """Request to search for objects."""
    
    query: Optional[str] = Field(
        None,
        description="Search query",
    )
    sort: Optional[Dict[str, Any]] = Field(
        None,
        description="Sort order for search results",
    )
    filter: Optional[Dict[str, Any]] = Field(
        None,
        description="Filter to apply to search results",
    )
    start_cursor: Optional[str] = Field(
        None,
        description="Pagination cursor",
    )
    page_size: Optional[int] = Field(
        None,
        description="Number of results to return per page",
    )


class ListBlocksRequest(BaseModel):
    """Request to list a block's children."""
    
    block_id: str = Field(..., description="The ID of the block to list children for")
    start_cursor: Optional[str] = Field(
        None,
        description="Pagination cursor",
    )
    page_size: Optional[int] = Field(
        None,
        description="Number of results to return per page",
    )


class AppendBlocksRequest(BaseModel):
    """Request to append blocks to a block's children."""
    
    block_id: str = Field(..., description="The ID of the block to append children to")
    children: List[Dict[str, Any]] = Field(
        ...,
        description="Children blocks to append",
    )


class UpdateBlockRequest(BaseModel):
    """Request to update a block."""
    
    block_id: str = Field(..., description="The ID of the block to update")
    content: Dict[str, Any] = Field(
        ...,
        description="Content to update",
    )


class DeleteBlockRequest(BaseModel):
    """Request to delete a block."""
    
    block_id: str = Field(..., description="The ID of the block to delete")


class CreateDatabaseRequest(BaseModel):
    """Request to create a database."""
    
    parent: Dict[str, Any] = Field(
        ...,
        description="Parent object (page_id)",
    )
    title: List[Dict[str, Any]] = Field(
        ...,
        description="Title of the database",
    )
    properties: Dict[str, Any] = Field(
        ...,
        description="Database properties schema",
    )
    icon: Optional[Dict[str, Any]] = Field(
        None,
        description="Icon object",
    )
    cover: Optional[Dict[str, Any]] = Field(
        None,
        description="Cover object",
    )
    is_inline: Optional[bool] = Field(
        None,
        description="Whether the database is inline",
    )


class UpdateDatabaseRequest(BaseModel):
    """Request to update a database."""
    
    database_id: str = Field(..., description="The ID of the database to update")
    title: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Title of the database",
    )
    properties: Optional[Dict[str, Any]] = Field(
        None,
        description="Database properties schema",
    )
    icon: Optional[Dict[str, Any]] = Field(
        None,
        description="Icon object",
    )
    cover: Optional[Dict[str, Any]] = Field(
        None,
        description="Cover object",
    )
    is_inline: Optional[bool] = Field(
        None,
        description="Whether the database is inline",
    )


class CreateCommentRequest(BaseModel):
    """Request to create a comment."""
    
    parent: Dict[str, Any] = Field(
        ...,
        description="Parent object (page_id or block_id)",
    )
    rich_text: List[Dict[str, Any]] = Field(
        ...,
        description="Rich text content of the comment",
    )
    discussion_id: Optional[str] = Field(
        None,
        description="ID of the discussion thread",
    )


class GetCommentRequest(BaseModel):
    """Request to get a comment."""
    
    comment_id: str = Field(..., description="The ID of the comment to get")


# Union type for all request types
RequestModel = Union[
    GetPageRequest,
    GetDatabaseRequest,
    QueryDatabaseRequest,
    GetBlockRequest,
    CreatePageRequest,
    UpdatePageRequest,
    SearchRequest,
    ListBlocksRequest,
    AppendBlocksRequest,
    UpdateBlockRequest,
    DeleteBlockRequest,
    CreateDatabaseRequest,
    UpdateDatabaseRequest,
    CreateCommentRequest,
    GetCommentRequest,
] 