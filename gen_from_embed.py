from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
from pprint import pprint
import os

load_dotenv()

PINECONE_INDEX = "faq-bot"
PROMPT_TEMPLATE = """
You are a chatbot designed for the website vivirdeingresospasivos.online. Your role is to educate users on passive income strategies, investment tools, and services offered on the site. Respond professionally and in a friendly tone. Support both Spanish and English. Answer questions about:

1. Automated copytrading systems (e.g., A10K, A100K).
2. Cryptocurrency tools (e.g., EazyBot, Daisy & Endotech).
3. The VIP Club, its benefits, and membership process.
4. Resources like investment portfolio templates.
5. Marc Barranco’s journey and philosophy on financial freedom.
Provide clear explanations, guide users to relevant resources on the website, and offer step-by-step assistance when needed. If the question is outside your scope, politely suggest contacting support or joining the VIP Club for expert help. Prioritize clarity, helpfulness, and accessibility.

Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {{question}}
"""
Q_SYSTEM = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(PINECONE_INDEX)

def generateFromEmbeddings(query_text="", model="gpt-4o-mini", chat_history=[]) -> tuple[str, list[str]]:
    
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", Q_SYSTEM),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = PineconeVectorStore(index=index, embedding=embedding_function)
    agent = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model=model)

    history_aware_retriever = create_history_aware_retriever(
        agent, db.as_retriever(), contextualize_q_prompt
    )


    
    qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PROMPT_TEMPLATE),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
    )
    question_answer_chain = create_stuff_documents_chain(agent, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    response = rag_chain.invoke({"input": query_text, "chat_history": chat_history})

    sources = response["context"]

    pprint(sources)
    response_text = response["answer"]
    return (response_text, sources)

def generateFromEmbeddingsWithoutHistory(query_text="", model="gpt-4o-mini") -> tuple[str, list[str]]:
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = PineconeVectorStore(index=index, embedding=embedding_function)
    agent = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model=model)

    qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PROMPT_TEMPLATE),
        ("human", "{input}"),
    ]
    )
    question_answer_chain = create_stuff_documents_chain(agent, qa_prompt)

    rag_chain = create_retrieval_chain(db.as_retriever(), question_answer_chain)

    response = rag_chain.invoke({"input": query_text})

    sources = response["context"]

    pprint(sources)
    response_text = response["answer"]
    return (response_text, sources)



