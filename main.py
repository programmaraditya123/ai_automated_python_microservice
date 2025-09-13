import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from fastapi import FastAPI
import requests
from pydantic import BaseModel
import os
from  Workflows.Mainworkflow import workflow,initial_state
from api.articles import getTitles
from typing import Literal
from services.pineconeretreiver.pinecone_retreiver import vector_search
from pymongo.mongo_client import MongoClient
from contextlib import asynccontextmanager
import certifi, os
import pinecone
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import time


origins = [
    "http://localhost:3000/",   # Next.js dev
    "https://knowledgepoll.site/",  # your deployed frontend domain
    "http://localhost:3000",   # Next.js dev
    "https://knowledgepoll.site",
]

 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("⏳ Starting services...")
    # MongoDB
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri, tlsCAFile=certifi.where())
    db = client["ArticleBlogPosts"]

    # Pinecone
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = pinecone.Pinecone(api_key=pinecone_api_key)

    # Store in app.state for global access
    app.state.client = client
    app.state.db = db
    app.state.pc = pc
    print("✅ Services initialized")

    yield  # Application runs here

    # Shutdown
    client.close()
    print("❌ MongoDB connection closed")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

class TopicRequest(BaseModel):
    title: str
    type: Literal["article","blog","post"]


@app.get('/')
def read_root():
    return {"Hello" : "World handling cors"}

@app.get('/preet')
def read_root():
    return {"Hello" : "bhai ji this microservice is hosted on googlecloud and use service cloudrun well"}

scheduler = BackgroundScheduler()

scheduler.add_job(getTitles,"interval",minutes=5)
scheduler.start()
 

@app.get('/get-title')
def read_root():
    return getTitles()
    

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
