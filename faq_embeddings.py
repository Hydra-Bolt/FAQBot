from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

from langchain.schema import Document
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Connect to your index
index_name = "faq-bot"
index = pc.Index(index_name)


def getTopK(query_text, k=3):
    embedding_function = OpenAIEmbeddings()
    db = PineconeVectorStore(index=index, embedding=embedding_function)

    responses = db.similarity_search_with_relevance_scores(query_text, k=k)
    return responses
