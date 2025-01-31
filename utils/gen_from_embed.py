from typing import List
from langchain.schema import Document
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

import os

load_dotenv()

PINECONE_INDEX = "faq-bot"
PROMPT_TEMPLATE = """
You are a knowledgeable and friendly chatbot for the website vivirdeingresospasivos.online for telegram. Do not use markdown in your resposne. Your primary role is to educate users on passive income strategies, investment tools, and services offered on the site. Respond professionally and in a friendly tone, supporting both Spanish and English languages. Club VIP is not a strategy.

Here are some of the strategies and services you should be familiar with:

ESTRATEGIAS A10K // A100K // CLUB VIP

A10K - INGRESO PASIVO  
Estrategia algorítmica en Forex  
Depósito mínimo: 2000 USD  
Beneficio mensual: 130-200 USD  
DD Riesgo: 14%  

A10K INTERÉS COMPUESTO  
Estrategia manual multidivisa en Forex  
Depósito mínimo: 1500 USD  
Beneficio mensual: 5-15% 
DD Riesgo: 50%

Please note that [WE NEVER OFFER] advice or support in the VIP Club. The VIP Club and A10K copytrading strategies are the same (it is a package). DO NOT USE ANY TYPE OF MARKDOWN FORMAT OR ANY SYMBOLS TO .
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


def generateFromEmbeddings(
    query_text="", model="gpt-4o-mini", chat_history=[]
) -> tuple[str, list[str]]:

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
    response_text = response["answer"]
    return (response_text, sources)


def generateFromEmbeddingsWithoutHistory(
    query_text="", model="gpt-4o-mini"
) -> tuple[str, list[str]]:
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

    response_text = response["answer"]
    return (response_text, sources)


def generateAnswerFromSources(
    query_text: str, sources: List[Document], chat_history: list[str], model="gpt-4o-mini"
) -> str:
    agent = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model=model)

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROMPT_TEMPLATE),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(agent, qa_prompt)

    response = question_answer_chain.invoke(
        {"input": query_text, "chat_history": chat_history, "context": sources}
    )

    return response
