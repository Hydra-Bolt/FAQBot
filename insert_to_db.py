from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import uuid
import json


index_name = 'faq-bot'

load_dotenv()

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)
# Create a new index or connect to an existing one
index = pc.Index(name=index_name)


# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

vector_store = PineconeVectorStore(index=index, embedding=OpenAIEmbeddings())   

# Load FAQ data from JSON file
with open('faq.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

# Create documents from FAQ data
documents = []
for item in faq_data:
    question = item['question']
    answer = item['response']
    text = f"Question: {question}\nAnswer: {answer}"
    documents.append({"text": text})

# Generate UUIDs for documents
for doc in documents:
    doc['id'] = str(uuid.uuid4())

# Insert documents into Pinecone
for doc in documents:
    ids = vector_store.add_texts([doc['text']], ids=[doc['id']])

print("Documents inserted successfully.", ids)