from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
# from models.posts_model import PostResponse
from models.postmodel import PostResponse
# from ..Prompts.Posts_Prompt.Post_structure_prompt import post_prompt
# from Prompts.poststructureprompt import post_prompt
# from Prompts.poststructureprompt import post_prompt
from services.Prompts.poststructureprompt import post_prompt
# from clients.mongodb_client import posts_collection
from client.mongodbClient import posts_collection
from langchain.output_parsers import RetryOutputParser

model = ChatOpenAI()

parser = PydanticOutputParser(pydantic_object=PostResponse)

# retry_out_parser = RetryOutputParser.from_llm(parser=parser,llm=model)

chain = post_prompt | model | parser

def savePost(post:PostResponse):
    post_dict = post.model_dump()
    result = posts_collection.insert_one(post_dict)
    return str(result.inserted_id)

def generatePost(topic:str):
    post = chain.invoke({'topic':topic})
    post_id = savePost(post)
    print("post saved with id :",{post_id})
    return {"post":post,"_id_":post_id}


