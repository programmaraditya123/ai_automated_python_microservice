from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()


class Topic(BaseModel):
    title: str = Field(description="The catchy, trending article title")
    type: Literal["article", "blog", "post"] = Field(
        description="The best suited format for this topic: 'article' (informative & structured), 'blog' (personal, opinionated, casual), or 'post' (short, punchy, social-media friendly)"
    )


class Topics(BaseModel):
    topics: list[Topic] = Field(description="List of trending article/blog/post ideas")


parser = PydanticOutputParser(pydantic_object=Topics)


def get_titles(v_title, v_description, v_comments):
    prompt = PromptTemplate(
        template="""
    You are an expert social media and trends analyst. 
    You are given the title, description, and audience comments from a YouTube video.  
    Your task is to analyze them to identify viral and trending angles for creating new content.

    Consider:
    - Current and emerging topics from the content
    - Emotional triggers or opinions in comments
    - Popular culture references
    - Keywords likely to attract attention

    Video Title: {title}
    Video Description: {description}
    Viewer Comments: {comments}

    Based on this, generate a list of content ideas with:
    - "title": a catchy, click-worthy title
    - "type": whether it’s best as an "article", "blog", or "post"

    Return only JSON in the required format.
    {format_instructions}
    """,
        input_variables=['title', 'description', 'comments'],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | model | parser

    response = chain.invoke({
        "title": v_title,
        "description": v_description,
        "comments": "\n".join(v_comments)
    })
    return response.dict()
