from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import FakeEmbeddings  # For local/dummy embeddings
import os

def get_vector_store():
    os.makedirs("data", exist_ok=True)
    file_path = "data/sample_docs.txt"

    # Ensure dummy data exists
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("This is a dummy research text for offline testing of RAG pipeline.")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    docs = [Document(page_content=chunk) for chunk in chunks]

    # Use local fake embeddings
    embeddings = FakeEmbeddings(size=384)  # 384-dim fake vectors
    vectorstore = Chroma.from_documents(docs, embedding=embeddings)

    return vectorstore

def rag_agent(state):
    query = state["context"]["user_query"]
    retriever = get_vector_store().as_retriever()
    docs = retriever.invoke(query)
    content = "\n\n".join([doc.page_content for doc in docs])
    state["context"]["rag_results"] = content
    return state
