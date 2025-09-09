from pydantic import BaseModel, Field
from typing import List, Optional


class BlogSection(BaseModel):
    heading: Optional[str] = Field(
        None,
        description="The section title or sub-heading of the blog.",
        example="Why Next.js is the Future of Web Development"
    )
    content: Optional[str] = Field(
        None,
        description="The main written content of this section.",
        example="Next.js has revolutionized web development by introducing server-side rendering and static site generation..."
    )
    bullets: Optional[List[str]] = Field(
        default_factory=list,
        description="Supporting bullet points or highlights for this section.",
        example=["Improved SEO", "Faster performance", "Better developer experience"]
    )


class BlogResponse(BaseModel):
    title: Optional[str] = Field(
        None,
        description="An eye-catching and SEO-friendly blog title.",
        example="5 Reasons Why Next.js Will Dominate Web Development in 2026"
    )
    introduction: Optional[str] = Field(
        None,
        description="A compelling introduction to hook the reader.",
        example="Web development is evolving faster than ever, and Next.js is at the forefront of this transformation..."
    )
    sections: Optional[List[BlogSection]] = Field(
        default_factory=list,
        description="The main body of the blog, divided into structured sections."
    )
    conclusion: Optional[str] = Field(
        None,
        description="A closing statement that summarizes the key points and reinforces the blog's message.",
        example="Next.js isn’t just another framework—it’s shaping the future of web development. Now is the best time to learn it!"
    )
    key_takeaways: Optional[List[str]] = Field(
        default_factory=list,
        description="A concise list of the most important points readers should remember.",
        example=["Next.js improves SEO", "It offers hybrid rendering", "The community is rapidly growing"]
    )
