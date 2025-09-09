#Mongo connection
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

uri = os.getenv('MONGODB_URI')

client = MongoClient(uri,tlsCAFile=certifi.where())
db = client['ArticleBlogPosts']
articles_collection = db["articles"]
blogs_collection = db["blogs"]
posts_collection = db["posts"]
embeddings_collection = db["embeddings"]

#test connection
try:
    client.admin.command('ping')
    print("Connected to mongodb through python microservice")
except Exception as e:
    print("COnnection error",e)