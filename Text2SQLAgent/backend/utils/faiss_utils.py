from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def retrieve_relevant_chunks(vectorstore: FAISS, query: str, k: int = 5):
    """
    Search the FAISS vectorstore for top-k relevant schema chunks.
    """
    embedding_model = OpenAIEmbeddings()
    return vectorstore.similarity_search(query, k=k)
