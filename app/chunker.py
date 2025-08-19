from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

def text_to_docs(text, chunk_size=800, chunk_overlap=120, metadata=None):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    docs = []
    for i, c in enumerate(chunks):
        meta = metadata.copy() if metadata else {}
        meta.update({"chunk": i})
        docs.append(Document(page_content=c, metadata=meta))
    return docs
