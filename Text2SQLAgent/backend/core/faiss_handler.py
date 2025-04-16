# faiss_handler.py
# backend/core/faiss_handler.py

import os
import faiss
import pickle
import numpy as np
from typing import List
from openai import OpenAI
import tiktoken  # Optional, for token counting
from core.logger import get_logger

logger = get_logger(__name__)

VECTOR_STORE_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "schema.index")
META_PATH = os.path.join(VECTOR_STORE_DIR, "schema_meta.pkl")

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []

        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self._load_index()
        else:
            self._init_new_index()

    def _init_new_index(self):
        os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
        self.index = faiss.IndexFlatL2(1536)  # OpenAI embedding dimension
        self.metadata = []
        self._save_index()

    def _save_index(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def _load_index(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def reset_db(self):
        self._init_new_index()

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        client = OpenAI()
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-ada-002"
        )
        return [e.embedding for e in response.data]

    def store_schema(self, chunks: List[dict]):
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self._get_embeddings(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        self.metadata.extend(chunks)
        self._save_index()

    def search(self, query: str, k: int = 5) -> List[dict]:
        embeddings = self._get_embeddings([query])
        distances, indices = self.index.search(np.array(embeddings).astype("float32"), k)
        results = []
        for i in indices[0]:
            if 0 <= i < len(self.metadata):
                results.append(self.metadata[i])
        return results
