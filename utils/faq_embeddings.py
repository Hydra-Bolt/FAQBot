from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

INDEX = "faq-bot"
index = pc.Index(INDEX)
embedding_function = OpenAIEmbeddings()

db = PineconeVectorStore(index=index, embedding=embedding_function)

def getTopK(query_text, k=3):
    responses = db.similarity_search_with_relevance_scores(query_text, k=k)
    return responses

def insertFAQ(ids, texts):
    try:
        resp = db.add_texts(texts, ids=ids)
        if resp:
            print(f"Added {texts} to the index")
            return True
    except Exception as e:
        print(f"Failed to add texts: {e}")
    return False

def deleteFAQ(id):
    try:
        db.delete([id])
        print(f"Deleted {id} from the index")
        return True
    except Exception as e:
        print(f"Failed to delete id {id}: {e}")
    return False