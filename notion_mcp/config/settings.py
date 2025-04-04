"""Settings for the Notion MCP server."""

import os
from typing import Optional

from pydantic import BaseModel, Field, validator


class NotionConfig(BaseModel):
    """Configuration for the Notion API."""
    
    api_key: str = Field(
        default_factory=lambda: os.environ.get("NOTION_API_KEY", ""),
        description="Notion API key for authentication",
    )
    api_version: str = Field(
        default="2022-06-28",
        description="Notion API version",
    )
    base_url: str = Field(
        default="https://api.notion.com",
        description="Base URL for the Notion API",
    )
    
    @validator("api_key")
    def validate_api_key(cls, v: str) -> str:
        """Validate that the API key is not empty."""
        if not v:
            raise ValueError(
                "Notion API key is required. Set it using the NOTION_API_KEY "
                "environment variable."
            )
        return v


class MCPServerConfig(BaseModel):
    """Configuration for the MCP server."""
    
    host: str = Field(
        default="0.0.0.0",
        description="Host to bind the server to",
    )
    port: int = Field(
        default=8000,
        description="Port to bind the server to",
    )
    debug: bool = Field(
        default=False,
        description="Whether to run in debug mode",
    )


class Settings(BaseModel):
    """Global settings for the application."""
    
    notion: NotionConfig = Field(
        default_factory=NotionConfig,
        description="Notion API configuration",
    )
    server: MCPServerConfig = Field(
        default_factory=MCPServerConfig,
        description="MCP server configuration",
    )


# Create a global settings instance
settings = Settings() 