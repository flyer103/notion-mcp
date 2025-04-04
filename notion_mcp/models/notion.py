"""Models for Notion API objects."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class RichTextType(str, Enum):
    """Types of rich text objects."""
    
    TEXT = "text"
    MENTION = "mention"
    EQUATION = "equation"


class TextColor(str, Enum):
    """Text colors for rich text objects."""
    
    DEFAULT = "default"
    GRAY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    GRAY_BACKGROUND = "gray_background"
    BROWN_BACKGROUND = "brown_background"
    ORANGE_BACKGROUND = "orange_background"
    YELLOW_BACKGROUND = "yellow_background"
    GREEN_BACKGROUND = "green_background"
    BLUE_BACKGROUND = "blue_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"


class Annotations(BaseModel):
    """Text annotations for rich text objects."""
    
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: TextColor = TextColor.DEFAULT


class TextContent(BaseModel):
    """Content of a text rich text object."""
    
    content: str
    link: Optional[Dict[str, str]] = None


class RichText(BaseModel):
    """Rich text object in Notion."""
    
    type: RichTextType
    text: Optional[TextContent] = None
    annotations: Annotations = Field(default_factory=Annotations)
    plain_text: str
    href: Optional[str] = None


class PageParent(BaseModel):
    """Page parent object."""
    
    type: str = "page_id"
    page_id: str


class DatabaseParent(BaseModel):
    """Database parent object."""
    
    type: str = "database_id"
    database_id: str


class WorkspaceParent(BaseModel):
    """Workspace parent object."""
    
    type: str = "workspace"


Parent = Union[PageParent, DatabaseParent, WorkspaceParent]


class PropertyType(str, Enum):
    """Types of page properties."""
    
    TITLE = "title"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    PEOPLE = "people"
    FILES = "files"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    FORMULA = "formula"
    RELATION = "relation"
    ROLLUP = "rollup"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    LAST_EDITED_BY = "last_edited_by"


class TitleProperty(BaseModel):
    """Title property for a page."""
    
    id: str
    type: PropertyType = PropertyType.TITLE
    title: List[RichText] = Field(default_factory=list)


class RichTextProperty(BaseModel):
    """Rich text property for a page."""
    
    id: str
    type: PropertyType = PropertyType.RICH_TEXT
    rich_text: List[RichText] = Field(default_factory=list)


class NumberProperty(BaseModel):
    """Number property for a page."""
    
    id: str
    type: PropertyType = PropertyType.NUMBER
    number: Optional[float] = None


class CheckboxProperty(BaseModel):
    """Checkbox property for a page."""
    
    id: str
    type: PropertyType = PropertyType.CHECKBOX
    checkbox: bool = False


class URLProperty(BaseModel):
    """URL property for a page."""
    
    id: str
    type: PropertyType = PropertyType.URL
    url: Optional[str] = None


class SelectOption(BaseModel):
    """Option for a select property."""
    
    id: Optional[str] = None
    name: str
    color: Optional[str] = None


class SelectProperty(BaseModel):
    """Select property for a page."""
    
    id: str
    type: PropertyType = PropertyType.SELECT
    select: Optional[SelectOption] = None


class MultiSelectProperty(BaseModel):
    """Multi-select property for a page."""
    
    id: str
    type: PropertyType = PropertyType.MULTI_SELECT
    multi_select: List[SelectOption] = Field(default_factory=list)


Property = Union[
    TitleProperty,
    RichTextProperty,
    NumberProperty,
    SelectProperty,
    MultiSelectProperty,
    CheckboxProperty,
    URLProperty,
]


class Page(BaseModel):
    """Notion page object."""
    
    id: str
    object: str = "page"
    created_time: datetime
    last_edited_time: datetime
    archived: bool = False
    parent: Parent
    properties: Dict[str, Property]
    url: str


class Database(BaseModel):
    """Notion database object."""
    
    id: str
    object: str = "database"
    created_time: datetime
    last_edited_time: datetime
    title: List[RichText]
    properties: Dict[str, Any]
    url: str


class BlockType(str, Enum):
    """Types of blocks in Notion."""
    
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    TO_DO = "to_do"
    TOGGLE = "toggle"
    CODE = "code"
    QUOTE = "quote"
    CALLOUT = "callout"
    DIVIDER = "divider"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"
    BOOKMARK = "bookmark"
    EMBED = "embed"
    EQUATION = "equation"
    TABLE = "table"
    TABLE_ROW = "table_row"
    CHILD_PAGE = "child_page"
    CHILD_DATABASE = "child_database"
    LINK_TO_PAGE = "link_to_page"
    SYNCED_BLOCK = "synced_block"
    TEMPLATE = "template"
    LINK_PREVIEW = "link_preview"
    UNSUPPORTED = "unsupported"


class ParagraphBlock(BaseModel):
    """Paragraph block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    color: TextColor = TextColor.DEFAULT
    children: Optional[List[Any]] = None


class HeadingBlock(BaseModel):
    """Heading block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    color: TextColor = TextColor.DEFAULT
    is_toggleable: bool = False


class BulletedListItemBlock(BaseModel):
    """Bulleted list item block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    color: TextColor = TextColor.DEFAULT
    children: Optional[List[Any]] = None


class NumberedListItemBlock(BaseModel):
    """Numbered list item block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    color: TextColor = TextColor.DEFAULT
    children: Optional[List[Any]] = None


class ToDoBlock(BaseModel):
    """To-do block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    checked: bool = False
    color: TextColor = TextColor.DEFAULT
    children: Optional[List[Any]] = None


class CodeBlock(BaseModel):
    """Code block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    language: str = "plain text"
    caption: List[RichText] = Field(default_factory=list)


class QuoteBlock(BaseModel):
    """Quote block in Notion."""
    
    rich_text: List[RichText] = Field(default_factory=list)
    color: TextColor = TextColor.DEFAULT
    children: Optional[List[Any]] = None


BlockContent = Union[
    ParagraphBlock,
    HeadingBlock,
    BulletedListItemBlock,
    NumberedListItemBlock,
    ToDoBlock,
    CodeBlock,
    QuoteBlock,
]


class Block(BaseModel):
    """Block object in Notion."""
    
    id: str
    object: str = "block"
    created_time: datetime
    last_edited_time: datetime
    archived: bool = False
    has_children: bool = False
    type: BlockType
    paragraph: Optional[ParagraphBlock] = None
    heading_1: Optional[HeadingBlock] = None
    heading_2: Optional[HeadingBlock] = None
    heading_3: Optional[HeadingBlock] = None
    bulleted_list_item: Optional[BulletedListItemBlock] = None
    numbered_list_item: Optional[NumberedListItemBlock] = None
    to_do: Optional[ToDoBlock] = None
    code: Optional[CodeBlock] = None
    quote: Optional[QuoteBlock] = None 