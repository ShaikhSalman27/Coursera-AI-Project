"""
modules/vector_store.py
--------------------------
Text ko chunks me split karna aur FAISS vector store banake save karna.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_text_chunks(text):
    """Split raw text into overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)


def get_vector_store(text_chunks):
    """Generate embeddings for text chunks and save a local FAISS index."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("pass_index")
