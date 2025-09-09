from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
# from models.blog_model import BlogResponse
from models.blogmodel import BlogResponse
# from ..Prompts.Blog_Prompts.Blog_structure_prompt import blogprompt
from services.Prompts.blogstructureprompt import blogprompt
# from clients.mongodb_client import blogs_collection
from client.mongodbClient import blogs_collection

model = ChatOpenAI()

parser = PydanticOutputParser(pydantic_object=BlogResponse)

chain = blogprompt | model | parser

def saveBlog(blog:BlogResponse) -> str:
    blog_dict = blog.model_dump()
    result = blogs_collection.insert_one(blog_dict)
    return str(result.inserted_id)

def generateBlog(topic:str):
    blog = chain.invoke({'topic':topic})
    blog_id = saveBlog(blog)
    print(f"blog saved with id : {blog_id}")
    return {"blog":blog,"_id_":blog_id}
