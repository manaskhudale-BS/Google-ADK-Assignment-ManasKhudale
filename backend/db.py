import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def search_handbook(query):
    """Perform semantic search on stored Employee Handbook content"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory="./vector_db", embedding_function=embeddings)
    results = db.similarity_search(query, k=2)

    if not results:
        return "No relevant section found in the handbook."
    return " ".join([r.page_content for r in results])
