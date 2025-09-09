# from pinecone_vector_search.vector_search import vectorstore
from services.pinecone_vectorstore.vector_store import vectorstore

# Connect vectorstore
vectorstore = vectorstore

# Query
# query = "How to learn Golang in 2026"
def vector_search(query:str):
    return  vectorstore.similarity_search(query, k=10)

# print("LangChain Search Results:")
# for doc in docs:
#     print(doc.page_content)
#     print(doc.metadata)
