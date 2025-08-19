import os
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.prompts import EMAIL_PROMPT
from app.embeddings_store import get_embeddings, create_or_load_vectorstore, load_vectorstore
from app.chunker import text_to_docs
from app.scraper import scrape_text_from_url
from app.utils import get_env

TOP_K = int(get_env("TOP_K", 4))
LLM_MODEL = get_env("LLM_MODEL", "llama3")  # match your Ollama pulled model

def get_llm(model_name=None):
    model_name = model_name or LLM_MODEL
    # LangChain Ollama LLM wrapper
    # Make sure you have ollama server running locally
    llm = Ollama(model=model_name, base_url=get_env("OLLAMA_HOST", "http://localhost:11434"))
    return llm

def ensure_vectorstore_for_url(url, force_reindex=False):
    """
    Scrape a URL, chunk into documents, and save to vectorstore if not already present.
    For demo, we store everything under one vectorstore directory. You can also
    partition by hostname.
    """
    persist_dir = get_env("VECTORSTORE_DIR", "./vectorstore")
    vs = load_vectorstore(persist_directory=persist_dir)
    if vs and not force_reindex:
        return vs
    text = scrape_text_from_url(url)
    docs = text_to_docs(text, metadata={"source": url})
    embeddings = get_embeddings()
    vect = create_or_load_vectorstore(documents=docs, persist_directory=persist_dir, embeddings=embeddings)
    return vect

def generate_cold_email(url, name, role, portfolio_links="", tone="professional", llm=None, top_k=TOP_K):
    llm = llm or get_llm()
    vect = ensure_vectorstore_for_url(url)
    retriever = vect.as_retriever(search_kwargs={"k": top_k})
    # Build prompt
    prompt = EMAIL_PROMPT.substitute(context="{context}", name=name, role=role, portfolio=portfolio_links or "N/A", tone=tone)
    # We will use a small retrieval QA wrapper: retrieve top docs, inject context into prompt, then call LLM
    docs = retriever.get_relevant_documents(role + " " + url)  # query with role + url to bias retrieval
    context_text = "\n\n---\n\n".join([d.page_content for d in docs[:top_k]])
    final_prompt = prompt.replace("{context}", context_text)
    # Simple LLM call
    out = llm(final_prompt)
    # If Ollama returns dict or object, convert to str
    if isinstance(out, dict) and "content" in out:
        return out["content"]
    return str(out)
