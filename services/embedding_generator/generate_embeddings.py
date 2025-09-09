from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")



def generate_embedding(text:str):
    generated_embedding = embeddings.embed_query(text)
    return generated_embedding


