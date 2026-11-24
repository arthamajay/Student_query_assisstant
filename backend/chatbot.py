import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Resolve paths relative to this file so the module works
# regardless of the working directory it is launched from.
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR.parent / ".env")

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
VECTOR_DB_DIR = str(BASE_DIR / "vector_db_dir")


def setup_vectorstore():
    embeddings = HuggingFaceEmbeddings()
    return Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings,
    )


def create_chain():
    vectorstore = setup_vectorstore()

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
    )

    return chain
