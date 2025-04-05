"""Notion API client for interacting with the Notion API."""

import json
from typing import Any, Dict, List, Optional, Union, cast

import requests
from pydantic import BaseModel

from notion_mcp.config.settings import settings
from notion_mcp.models.notion import Block, Database, Page


class NotionAPIError(Exception):
    """Exception raised when the Notion API returns an error."""
    
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Notion API Error ({status_code}): {message}")


class SearchParams(BaseModel):
    """Parameters for the search endpoint."""
    
    query: Optional[str] = None
    sort: Optional[Dict[str, Any]] = None
    filter: Optional[Dict[str, Any]] = None
    start_cursor: Optional[str] = None
    page_size: Optional[int] = None


class ListBlocksParams(BaseModel):
    """Parameters for the list blocks endpoint."""
    
    start_cursor: Optional[str] = None
    page_size: Optional[int] = None


class NotionClient:
    """Client for interacting with the Notion API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_version: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """Initialize the Notion client."""
        self.api_key = api_key or settings.notion.api_key
        self.api_version = api_version or settings.notion.api_version
        self.base_url = base_url or settings.notion.base_url
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": self.api_version,
            "Content-Type": "application/json",
        })
    
    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request to the Notion API.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            path: API path
            params: Query parameters
            data: Request body data
            
        Returns:
            Response data
            
        Raises:
            NotionAPIError: If the API returns an error
        """
        url = f"{self.base_url}{path}"
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=data,
        )
        
        if not response.ok:
            try:
                error_data = response.json()
                message = error_data.get("message", "Unknown error")
            except json.JSONDecodeError:
                message = response.text or "Unknown error"
            
            raise NotionAPIError(
                status_code=response.status_code,
                message=message,
            )
        
        return response.json()
    
    def search(self, params: Optional[SearchParams] = None) -> Dict[str, Any]:
        """Search for objects in Notion.
        
        Args:
            params: Search parameters
            
        Returns:
            Search results
        """
        data = params.dict(exclude_none=True) if params else {}
        return self._make_request("POST", "/v1/search", data=data)
    
    def get_page(self, page_id: str) -> Page:
        """Get a page by ID.
        
        Args:
            page_id: Page ID
            
        Returns:
            Page object
        """
        response = self._make_request("GET", f"/v1/pages/{page_id}")
        return Page(**response)
    
    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Page:
        """Update a page's properties.
        
        Args:
            page_id: Page ID
            properties: Properties to update
            
        Returns:
            Updated page object
        """
        response = self._make_request(
            "PATCH",
            f"/v1/pages/{page_id}",
            data={"properties": properties},
        )
        return Page(**response)
    
    def get_database(self, database_id: str) -> Database:
        """Get a database by ID.
        
        Args:
            database_id: Database ID
            
        Returns:
            Database object
        """
        response = self._make_request("GET", f"/v1/databases/{database_id}")
        return Database(**response)
    
    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query a database.
        
        Args:
            database_id: Database ID
            filter: Filter to apply
            sorts: Sort order
            start_cursor: Pagination cursor
            page_size: Page size
            
        Returns:
            Query results
        """
        data = {}
        if filter:
            data["filter"] = filter
        if sorts:
            data["sorts"] = sorts
        if start_cursor:
            data["start_cursor"] = start_cursor
        if page_size:
            data["page_size"] = page_size
        
        return self._make_request(
            "POST",
            f"/v1/databases/{database_id}/query",
            data=data,
        )
    
    def get_block(self, block_id: str) -> Block:
        """Get a block by ID.
        
        Args:
            block_id: Block ID
            
        Returns:
            Block object
        """
        response = self._make_request("GET", f"/v1/blocks/{block_id}")
        return Block(**response)
    
    def update_block(
        self,
        block_id: str,
        content: Dict[str, Any],
    ) -> Block:
        """Update a block's content.
        
        Args:
            block_id: Block ID
            content: Content to update
            
        Returns:
            Updated block object
        """
        response = self._make_request(
            "PATCH",
            f"/v1/blocks/{block_id}",
            data=content,
        )
        return Block(**response)
    
    def list_blocks(
        self,
        block_id: str,
        params: Optional[ListBlocksParams] = None,
    ) -> Dict[str, Any]:
        """List a block's children.
        
        Args:
            block_id: Block ID
            params: Pagination parameters
            
        Returns:
            List of children blocks
        """
        query_params = params.dict(exclude_none=True) if params else {}
        return self._make_request(
            "GET",
            f"/v1/blocks/{block_id}/children",
            params=query_params,
        )
    
    def append_blocks(
        self,
        block_id: str,
        children: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Append blocks to a block's children.
        
        Args:
            block_id: Block ID
            children: Children blocks to append
            
        Returns:
            Updated list of children blocks
        """
        return self._make_request(
            "PATCH",
            f"/v1/blocks/{block_id}/children",
            data={"children": children},
        )
    
    def delete_block(self, block_id: str) -> Block:
        """Delete a block.
        
        Args:
            block_id: Block ID
            
        Returns:
            Deleted block object
        """
        response = self._make_request("DELETE", f"/v1/blocks/{block_id}")
        return Block(**response)
    
    def create_page(
        self,
        parent: Dict[str, Any],
        properties: Dict[str, Any],
        children: Optional[List[Dict[str, Any]]] = None,
    ) -> Page:
        """Create a new page.
        
        Args:
            parent: Parent object (database_id or page_id)
            properties: Page properties
            children: Children blocks
            
        Returns:
            Created page object
        """
        data = {
            "parent": parent,
            "properties": properties,
        }
        if children:
            data["children"] = children
        
        response = self._make_request("POST", "/v1/pages", data=data)
        return Page(**response)
    
    def create_database(
        self,
        parent: Dict[str, Any],
        title: List[Dict[str, Any]],
        properties: Dict[str, Any],
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        is_inline: Optional[bool] = None,
    ) -> Database:
        """Create a new database.
        
        Args:
            parent: Parent object (page_id)
            title: Title of the database
            properties: Database properties schema
            icon: Icon object
            cover: Cover object
            is_inline: Whether the database is inline
            
        Returns:
            Created database object
        """
        data = {
            "parent": parent,
            "title": title,
            "properties": properties,
        }
        if icon:
            data["icon"] = icon
        if cover:
            data["cover"] = cover
        if is_inline is not None:
            data["is_inline"] = is_inline
        
        response = self._make_request("POST", "/v1/databases", data=data)
        return Database(**response)
    
    def update_database(
        self,
        database_id: str,
        title: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Dict[str, Any]] = None,
        cover: Optional[Dict[str, Any]] = None,
        is_inline: Optional[bool] = None,
    ) -> Database:
        """Update a database.
        
        Args:
            database_id: Database ID
            title: Title of the database
            properties: Database properties schema
            icon: Icon object
            cover: Cover object
            is_inline: Whether the database is inline
            
        Returns:
            Updated database object
        """
        data = {}
        if title:
            data["title"] = title
        if properties:
            data["properties"] = properties
        if icon:
            data["icon"] = icon
        if cover:
            data["cover"] = cover
        if is_inline is not None:
            data["is_inline"] = is_inline
        
        response = self._make_request(
            "PATCH",
            f"/v1/databases/{database_id}",
            data=data,
        )
        return Database(**response)
    
    def create_comment(
        self,
        parent: Dict[str, Any],
        rich_text: List[Dict[str, Any]],
        discussion_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a comment.
        
        Args:
            parent: Parent object (page_id or block_id)
            rich_text: Rich text content of the comment
            discussion_id: ID of the discussion thread
            
        Returns:
            Created comment object
        """
        data = {
            "parent": parent,
            "rich_text": rich_text,
        }
        if discussion_id:
            data["discussion_id"] = discussion_id
        
        return self._make_request("POST", "/v1/comments", data=data)
    
    def get_comment(self, comment_id: str) -> Dict[str, Any]:
        """Get a comment by ID.
        
        Args:
            comment_id: Comment ID
            
        Returns:
            Comment object
        """
        return self._make_request("GET", f"/v1/comments/{comment_id}") 