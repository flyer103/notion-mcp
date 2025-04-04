"""Utilities for working with Notion."""

from typing import Dict, List, Optional, Union

from notion_mcp.models.notion import (
    Annotations,
    RichText,
    RichTextType,
    TextContent,
)


def create_rich_text(
    content: str,
    link: Optional[str] = None,
    bold: bool = False,
    italic: bool = False,
    strikethrough: bool = False,
    underline: bool = False,
    code: bool = False,
    color: str = "default",
) -> RichText:
    """Create a rich text object.
    
    Args:
        content: Text content
        link: Optional URL to link to
        bold: Whether the text is bold
        italic: Whether the text is italic
        strikethrough: Whether the text has a strikethrough
        underline: Whether the text is underlined
        code: Whether the text is code
        color: Text color
        
    Returns:
        Rich text object
    """
    text_content = TextContent(
        content=content,
        link={"url": link} if link else None,
    )
    
    annotations = Annotations(
        bold=bold,
        italic=italic,
        strikethrough=strikethrough,
        underline=underline,
        code=code,
        color=color,
    )
    
    return RichText(
        type=RichTextType.TEXT,
        text=text_content,
        annotations=annotations,
        plain_text=content,
        href=link,
    )


def create_title_property(title: str) -> Dict[str, List[RichText]]:
    """Create a title property for a page.
    
    Args:
        title: Page title
        
    Returns:
        Title property
    """
    return {
        "title": [create_rich_text(title)],
    }


def create_rich_text_property(text: str) -> Dict[str, List[RichText]]:
    """Create a rich text property for a page.
    
    Args:
        text: Property text
        
    Returns:
        Rich text property
    """
    return {
        "rich_text": [create_rich_text(text)],
    }


def create_select_property(name: str) -> Dict[str, Dict[str, str]]:
    """Create a select property for a page.
    
    Args:
        name: Option name
        
    Returns:
        Select property
    """
    return {
        "select": {
            "name": name,
        },
    }


def create_multi_select_property(
    names: List[str],
) -> Dict[str, List[Dict[str, str]]]:
    """Create a multi-select property for a page.
    
    Args:
        names: Option names
        
    Returns:
        Multi-select property
    """
    return {
        "multi_select": [{"name": name} for name in names],
    }


def create_number_property(number: Union[int, float]) -> Dict[str, Union[int, float]]:
    """Create a number property for a page.
    
    Args:
        number: Number value
        
    Returns:
        Number property
    """
    return {
        "number": number,
    }


def create_checkbox_property(checked: bool) -> Dict[str, bool]:
    """Create a checkbox property for a page.
    
    Args:
        checked: Whether the checkbox is checked
        
    Returns:
        Checkbox property
    """
    return {
        "checkbox": checked,
    }


def create_url_property(url: str) -> Dict[str, str]:
    """Create a URL property for a page.
    
    Args:
        url: URL
        
    Returns:
        URL property
    """
    return {
        "url": url,
    }


def create_page_parent(page_id: str) -> Dict[str, str]:
    """Create a page parent object.
    
    Args:
        page_id: Page ID
        
    Returns:
        Page parent object
    """
    return {
        "type": "page_id",
        "page_id": page_id,
    }


def create_database_parent(database_id: str) -> Dict[str, str]:
    """Create a database parent object.
    
    Args:
        database_id: Database ID
        
    Returns:
        Database parent object
    """
    return {
        "type": "database_id",
        "database_id": database_id,
    }


def create_paragraph_block(text: str) -> Dict[str, Dict]:
    """Create a paragraph block.
    
    Args:
        text: Paragraph text
        
    Returns:
        Paragraph block
    """
    return {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [create_rich_text(text)],
        },
    }


def create_heading_block(
    text: str,
    level: int = 1,
    is_toggleable: bool = False,
) -> Dict[str, Dict]:
    """Create a heading block.
    
    Args:
        text: Heading text
        level: Heading level (1-3)
        is_toggleable: Whether the heading is toggleable
        
    Returns:
        Heading block
    """
    if level not in (1, 2, 3):
        raise ValueError("Heading level must be 1, 2, or 3")
    
    return {
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": [create_rich_text(text)],
            "is_toggleable": is_toggleable,
        },
    }


def create_bulleted_list_item(text: str) -> Dict[str, Dict]:
    """Create a bulleted list item block.
    
    Args:
        text: List item text
        
    Returns:
        Bulleted list item block
    """
    return {
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [create_rich_text(text)],
        },
    }


def create_numbered_list_item(text: str) -> Dict[str, Dict]:
    """Create a numbered list item block.
    
    Args:
        text: List item text
        
    Returns:
        Numbered list item block
    """
    return {
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": [create_rich_text(text)],
        },
    }


def create_to_do_block(text: str, checked: bool = False) -> Dict[str, Dict]:
    """Create a to-do block.
    
    Args:
        text: To-do text
        checked: Whether the to-do is checked
        
    Returns:
        To-do block
    """
    return {
        "type": "to_do",
        "to_do": {
            "rich_text": [create_rich_text(text)],
            "checked": checked,
        },
    }


def create_code_block(code: str, language: str = "plain text") -> Dict[str, Dict]:
    """Create a code block.
    
    Args:
        code: Code text
        language: Programming language
        
    Returns:
        Code block
    """
    return {
        "type": "code",
        "code": {
            "rich_text": [create_rich_text(code)],
            "language": language,
        },
    }


def create_quote_block(text: str) -> Dict[str, Dict]:
    """Create a quote block.
    
    Args:
        text: Quote text
        
    Returns:
        Quote block
    """
    return {
        "type": "quote",
        "quote": {
            "rich_text": [create_rich_text(text)],
        },
    } 