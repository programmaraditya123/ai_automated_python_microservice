from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from dotenv import load_dotenv
from services.article_generator import generateArticle
# from services.contentGenerator.Blog_generator import generateBlog
# from services.contentGenerator.post_generator import generatePost
from services.contentgenerator.postgenerator import generatePost
from services.contentgenerator.Bloggenerator import generateBlog
# from services.emmbedding_generator.generate_embeddings import generate_embedding
from services.embedding_generator.generate_embeddings import generate_embedding
# from clients.mongodb_client import embeddings_collection
from langchain.schema import Document
# from services.pinecone_vector_search.vector_search import pc, index_name
from services.pinecone_vectorstore.vector_store import pc,index_name

load_dotenv()

index = pc.Index(index_name)


class TitleType(TypedDict):
    title: str
    type: Literal["article", "blog", "post"]
    content: dict
    _id_: int
    combined_text: str
    embedding: list[float]


def condition_checker(state: TitleType) -> Literal["generate_article", "generate_blog", "generate_post"]:
    if state["type"] == "article":
        return "generate_article"
    elif state["type"] == "post":
        return "generate_post"
    elif state["type"] == "blog":
        return "generate_blog"


def generate_article(state: TitleType):
    content = generateArticle(state["title"])
    return {"content": content["article"], "_id_": content["_id_"]}


def generate_blog(state: TitleType):
    content = generateBlog(state["title"])
    return {"content": content["blog"],"_id_": content["_id_"]}


def generate_post(state: TitleType):
    content = generatePost(state["title"])
    return {'content': content["post"],"_id_": content["_id_"]}


def generate_embedding_data(state: TitleType):
    title = state["title"]
    # Could be Article, BlogResponse, or PostResponse
    content_obj = state["content"]

    parts = [title]

    # Handle Article
    if state["type"] == "article":
        parts.append(getattr(content_obj, "introduction", ""))

        if hasattr(content_obj, "sections") and content_obj.sections:
            for section in content_obj.sections:
                parts.append(getattr(section, "heading", "") or "")
                parts.append(getattr(section, "summary", "") or "")
                parts.append(getattr(section, "details", "") or "")

                if getattr(section, "subsections", None):
                    for sub in section.subsections:
                        parts.append(getattr(sub, "subheading", "") or "")
                        parts.append(getattr(sub, "text", "") or "")
                        if getattr(sub, "list_items", None):
                            parts.extend(sub.list_items)

        parts.append(getattr(content_obj, "conclusion", ""))

    # Handle Blog
    elif state["type"] == "blog":
        parts.append(getattr(content_obj, "introduction", ""))
        if hasattr(content_obj, "sections") and content_obj.sections:
            for section in content_obj.sections:
                parts.append(getattr(section, "heading", ""))
                parts.append(getattr(section, "content", ""))
                if getattr(section, "bullets", None):
                    parts.extend(section.bullets)
        parts.append(getattr(content_obj, "conclusion", ""))

    # Handle Post
    elif state["type"] == "post":
        parts.append(getattr(content_obj, "body", ""))
        if getattr(content_obj, "hashtags", None):
            parts.extend(content_obj.hashtags)

    # Combine everything
    combined_text = f"{title}\n\n" + "\n\n".join([p for p in parts if p])
    embedding = generate_embedding(combined_text)

    return {
        "embedding": embedding,
        "combined_text": combined_text
    }


def save_embedding_to_db(state: TitleType):
    index.upsert(
        vectors=[{
            "id":str(state["_id_"]),
            "values": state["embedding"],
            "metadata": {
                "title": state["title"],
                "type": state["type"],
                "id": state["_id_"],
                "text": state["title"]
            }
        }]
    )
    return state
    # doc = {
    #     "d_id":state["_id_"],
    #     "title":state["title"],
    #     "type":state["type"],
    #     "embedding":state["embedding"]
    # }
    # embeddings_collection.insert_one(doc)


graph = StateGraph(TitleType)


# add sequential nodes of Writing Article
graph.add_node("generate_article", generate_article)

# add sequential nodes of writing blogs
graph.add_node("generate_blog", generate_blog)

# add sequential node of writing posts
graph.add_node("generate_post", generate_post)

# add first conditional edge
graph.add_conditional_edges(START, condition_checker)

# add embedding node
graph.add_node("generate_embedding", generate_embedding_data)

# add node to save embedding to db
graph.add_node("save_embedding_to_db", save_embedding_to_db)

# add article flow edges
graph.add_edge("generate_article", "generate_embedding")

# add blog flow edges
graph.add_edge("generate_blog", "generate_embedding")


# add post flow edges
graph.add_edge("generate_post", "generate_embedding")

# add embedding generating edge
graph.add_edge("generate_embedding", "save_embedding_to_db")

# edge between generating embedding ---> save embedding to db
graph.add_edge("save_embedding_to_db", END)

workflow = graph.compile()


# initial_state1={
#     "title":"how to golang in 2026",
#     "type":"article"
# }

# res = workflow.invoke(initial_state1)
# print("8888888888",res)

def initial_state(title: str, type: str):
    return {"title": title, "type": type}
