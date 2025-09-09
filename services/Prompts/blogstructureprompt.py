from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.blogmodel import BlogResponse

parser = PydanticOutputParser(pydantic_object=BlogResponse)

blogprompt = PromptTemplate(
    template=(
        "You are an expert blogger, storyteller, and SEO strategist. "
        "Generate a **complete blog** in strict JSON format (without explanations, markdown, or quotes). "
        "The blog should be highly engaging, well-structured, and tailored to the given audience and tone. "
        "Ensure it flows naturally, keeps the reader hooked, and is easy to render in a React UI.\n\n"
        "Topic: {topic}\n"
        
        "Follow this exact JSON structure:\n"
        "{format_instructions}\n\n"
        "Constraints:\n"
        "- The `introduction` must be compelling, clear, and set expectations.\n"
        "- Each `section` must have a heading, detailed content, and optional bullets.\n"
        "- The `content` across all sections should approach the requested length 2000 words.\n"
        "- Use natural storytelling, examples, comparisons, and clear explanations.\n"
        "- The `conclusion` should summarize the key ideas and inspire action.\n"
        "- `key_takeaways` must be 3–5 concise, powerful points.\n"
        "- Do NOT include anything outside the JSON structure."
    ),
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
