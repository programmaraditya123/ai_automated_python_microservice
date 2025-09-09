from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class TableRow(BaseModel):
    columns: List[str] = Field(..., description="List of values for each column")


class Table(BaseModel):
    title: str = Field(..., description="Title of the table")
    headers: List[str] = Field(..., description="Column headers")
    rows: List[TableRow] = Field(..., description="Table rows")


class SubSection(BaseModel):
    subheading: str = Field(..., description="Subsection heading (h2, h3, etc.)")
    text: str = Field(..., description="Subsection details")
    list_items: Optional[List[str]] = Field(None, description="Bullet or numbered list items under this subsection")
    tables: Optional[List[Table]] = Field(None, description="Tables relevant to this subsection")


class Section(BaseModel):
    heading: str = Field(..., description="Main section heading (h1)")
    summary: Optional[str] = Field(None, description="Why this section is important / preview")
    details: Optional[str] = Field(None, description="Full detailed content for this section")  # 👈 FIXED
    types: Optional[List[str]] = Field(None, description="Types if applicable")
    advantages: Optional[List[str]] = Field(None, description="Advantages list if applicable")
    disadvantages: Optional[List[str]] = Field(None, description="Disadvantages list if applicable")
    subsections: Optional[List[SubSection]] = Field(None, description="Optional nested subsections")
    tables: Optional[List[Table]] = Field(None, description="Tables relevant to this section")



class SEO(BaseModel):
    title: str = Field(..., description="SEO title")
    description: str = Field(..., description="SEO description")
    keywords: List[str] = Field(..., description="SEO keywords")

# A reply to a comment
class Reply(BaseModel):
    user: str = Field(..., description="User who replied")
    text: str = Field(..., description="Reply content")
    created_at: datetime = Field(default_factory=datetime.now, description="Reply timestamp")

# A top-level comment
class Comment(BaseModel):
    user: str = Field(..., description="User who commented")
    text: str = Field(..., description="Comment content")
    created_at: datetime = Field(default_factory=datetime.now, description="Comment timestamp")
    replies: List[Reply] = Field(default=[], description="Replies to this comment")

# Wrapper for all comments
class Comments(BaseModel):
    comments: List[Comment] = Field(default=[], description="List of comments on the article")

# Views, likes, dislikes, etc.
class Views(BaseModel):
    views: int = Field(default=0, description="How many views the article got")
    likes: int = Field(default=0, description="How many likes the article got")
    dislikes: int = Field(default=0, description="How many dislikes the article got")
    churn_rate: float = Field(default=0.0, description="Churn rate of the article (percentage)")

class Article(BaseModel):
    title: str = Field(..., description="Main article title")
    author: str = Field(default="AI Generator", description="Author of the article")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    introduction: str = Field(..., description="Introduction text for the article")
    sections: List[Section] = Field(..., description="Main content sections of the article")
    conclusion: str = Field(..., description="Final conclusion of the article")
    seo: SEO
    comments: Comments = Field(default_factory=Comments, description="Comments on the article")
    views: Views = Field(default_factory=Views, description="Article engagement metrics")


