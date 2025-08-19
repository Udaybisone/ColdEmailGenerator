import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3  # 👈 patch before chroma import

import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from app.utils import get_env, ensure_dir

EMBED_MODEL = get_env("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
PERSIST_DIR = get_env("VECTORSTORE_DIR", "./vectorstore")

def get_embeddings():
    # Use HuggingFace local/transformers-based embeddings (free)
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def create_or_load_vectorstore(documents, persist_directory=PERSIST_DIR, embeddings=None):
    ensure_dir(persist_directory)
    embeddings = embeddings or get_embeddings()
    # Build Chroma vectorstore and persist
    vect = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=persist_directory)
    vect.persist()
    return vect

def load_vectorstore(persist_directory=PERSIST_DIR, embeddings=None):
    embeddings = embeddings or get_embeddings()
    if not os.path.exists(persist_directory):
        return None
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
