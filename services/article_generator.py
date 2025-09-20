#llm prompt for generating articles
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
from client.mongodbClient import articles_collection
from models.articlesmodel import Article

load_dotenv()

# model = ChatOpenAI()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = PydanticOutputParser(pydantic_object=Article)

prompt = PromptTemplate(
    template = (
    "You are an expert content writer and SEO specialist. "
    "Generate a **structured article** in strict JSON format (without explanations, markdown, or quotes). "
    "The article should be at least 1000 words long, well-organized, and highly engaging so it can be easily rendered in a React UI. "
    "Write in a way that captures attention, keeps readers hooked, and provides value. "
    "Ensure smooth flow with subheadings, bullet points, and clear formatting inside the JSON.\n\n"
    "Topic: {topic}\n\n"
    "Follow this exact JSON structure:\n"
    "{format_instructions}\n\n"
    "Constraints:\n"
    "- The `content` must be at least 1000 words.\n"
    "- The article should include multiple sections with headings, subheadings, and paragraphs.\n"
    "- Use natural storytelling, examples, and clear explanations.\n"
    "- Make sure `seo` fields are optimized and concise.\n"
    "- Do NOT include anything outside the JSON structure."
    ),
    input_variables=['topic'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

chain = prompt | model | parser 

def saveArticle(article:Article) -> str:
    article_dict = article.model_dump()
    result = articles_collection.insert_one(article_dict)
    return str(result.inserted_id)



def generateArticle(topic:str):
    article = chain.invoke({'topic':topic})
    article_id = saveArticle(article)
    print(f"Article saved with id :{article_id}")
    return {"article":article,"_id_":article_id}