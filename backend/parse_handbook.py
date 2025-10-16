from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

# Load the handbook PDF
print("Parsing Employee Handbook...")
loader = PyPDFLoader("./data/Employee_Handbook.pdf")
docs = loader.load()

# Split text into manageable chunks (≈500–800 characters)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " "]
)
splits = text_splitter.split_documents(docs)
print(f"Extracted {len(splits)} chunks from handbook.")

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create Chroma DB
db = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./vector_db"
)

print("Handbook data embedded and stored successfully!")
