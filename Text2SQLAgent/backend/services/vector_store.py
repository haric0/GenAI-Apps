import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle
from core.logger import get_logger

logger = get_logger(__name__)

class VectorStoreService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_path = "vector_store/schema.index"
        self.meta_path = "vector_store/metadata.pkl"
        self.index = None
        self.metadata = []
        self.load_index()

    def load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)
            logger.info("FAISS index and metadata loaded successfully.")
        else:
            self.index = faiss.IndexFlatL2(384)
            logger.info("New FAISS index created with dimension 384.")

    def reset_db(self):
        self.index = faiss.IndexFlatL2(384)
        self.metadata = []
        self.save_index()
        logger.info("Vector store reset successfully.")

    def store_schema(self, schema_chunks: list):
        embeddings = self.model.encode(schema_chunks, convert_to_numpy=True)
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata = schema_chunks
        self.save_index()
        logger.info(f"Stored {len(schema_chunks)} schema chunks into vector store.")

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        logger.info("Index and metadata saved to disk.")

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.metadata[i] for i in indices[0] if i < len(self.metadata)]

    def query(self, text: str, top_k: int = 3):
        logger.info(f"Calling Query in Vector Store, Query Received: {text}")

        try:
            if not self.index or not self.metadata:
                raise ValueError("FAISS index or metadata not found. Please upload schema first.")

            if not hasattr(self, "model") or self.model is None:
                raise ValueError("Embedding model is not initialized.")

            embedding = self.model.encode([text], convert_to_numpy=True).astype("float32")
            if embedding.shape[1] != self.index.d:
                raise ValueError(f"Embedding dimension mismatch: expected {self.index.d}, got {embedding.shape[1]}")

            logger.info(f"Query Embedding Completed: shape={embedding.shape}")

            D, I = self.index.search(embedding, top_k)
            logger.info(f"Query Search Results (Distances and Indices): {D}, {I}")

            results = [self.metadata[i] for i in I[0] if i < len(self.metadata)]
            logger.info(f"Query Results: {results}")

            return results

        except Exception as e:
            logger.error(f"Error during FAISS query: {e}", exc_info=True)
            return []
