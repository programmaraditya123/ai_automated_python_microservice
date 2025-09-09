from pydantic import BaseModel, Field
from typing import List, Optional


class PostRequest(BaseModel):
    """Request schema for generating a post"""
    topic: Optional[str] = Field(
        None,
        description="The main topic or theme of the post"
    )


class PostResponse(BaseModel):
    """Response schema for generated posts"""
    title: Optional[str] = Field(
        None,
        description="Catchy title or headline for the post. Must be a short sentence."
    )
    body: Optional[str] = Field(
        None,
        description="Main content of the post. Should be engaging, scannable, and audience-friendly."
    )
    hashtags: Optional[List[str]] = Field(
        default_factory=list,
        description="Relevant hashtags for engagement. Provide only words starting with '#'."
    )
