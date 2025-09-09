from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.postmodel import PostResponse


parser = PydanticOutputParser(pydantic_object=PostResponse)

post_prompt = PromptTemplate(
    template="""
You are a creative content writer. 
Write a short, engaging, and highly shareable post.

Topic: {topic}

Return the output as **valid JSON only**.  
Do not add comments, markdown formatting, or extra text.  
Do not include trailing commas.  

{format_instructions}

### Instructions:
1. Start with a **hook or bold statement**.
2. Keep it **concise and scannable** (short sentences, emojis if relevant).
3. Use **hashtags or keywords** for discoverability (LinkedIn, Twitter, Instagram).
4. Maintain the tone according to the topic.
5. End with a **call-to-action**.
6. Ensure suitability for all audiences.
""",
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
