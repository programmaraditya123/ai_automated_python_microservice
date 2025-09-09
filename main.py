import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from fastapi import FastAPI
import requests
from pydantic import BaseModel
import os
# from Workflows.MainWorkflow import workflow,initial_state
from  Workflows.Mainworkflow import workflow,initial_state
from api.articles import getTitles
from typing import Literal
# from services.pinecone_retreiver.pinecone_retreiver import vector_search
from services.pineconeretreiver.pinecone_retreiver import vector_search
app = FastAPI()

 
 

class TopicRequest(BaseModel):
    title: str
    type: Literal["article","blog","post"]


@app.get('/')
def read_root():
    return {"Hello" : "World"}

@app.get('/preet')
def read_root():
    return {"Hello" : "bhai ji this microservice is hosted on googlecloud and use service cloudrun well"}


 

@app.get('/get-title')
def read_root():
    return getTitles()
    
     

# @app.post('/generateArticle')
# async def read_root(topic:dict):
#     return generateArticle(topic)

@app.post('/generateArticle')
async def read_root(req:TopicRequest):
    print(req.model_dump(),"666666666666666")
    state =  initial_state(title=req.title,type=req.type)
    result = workflow.invoke(state)
    return result
    

@app.get('/recommendation')
async def read_root(query:str):
    return vector_search(query)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Default to 8080 if PORT not set
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
