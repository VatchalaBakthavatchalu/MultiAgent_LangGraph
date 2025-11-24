from retrieval.search import Search
from typing import List,Dict,Any
import numpy as np


class SemanticSearch(Search):
    """Semantic embedding-based search implementation"""

    def __init__(self, embedding_model=None):
        self.documents = []
        self.embeddings = []
        self.embedding_model = embedding_model

    def build_index(self, documents: List[str]) -> None:
        """Build semantic search index by embedding all documents"""
        if self.embedding_model is None:
            raise ValueError("Embedding model not provided in __init__")

        self.documents = documents
        # Pre-compute embeddings for all documents
        self.embeddings = []
        for doc in documents:
            embedding = self.embedding_model.embed_query(doc)
            self.embeddings.append(embedding)

        self.embeddings = np.array(self.embeddings)
        print(f"✓ Semantic index built with {len(documents)} documents")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search using semantic similarity with cosine distance"""
        if len(self.embeddings) == 0:
            raise ValueError("Index not built. Call build_index() first.")

        # Embed query
        query_embedding = np.array(
            self.embedding_model.embed_query(query)
        )

        # Calculate cosine similarity with all documents
        similarities = []
        for doc_embedding in self.embeddings:
            # Cosine similarity: (A·B) / (||A|| ||B||)
            similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding) + 1e-9
            )
            similarities.append(similarity)

        similarities = np.array(similarities)
        # Get top k results
        top_indices = np.argsort(similarities)[-k:][::-1]

        return [
            {
                "content": self.documents[idx],
                "score": float(similarities[idx]),
                "index": int(idx)
            }
            for idx in top_indices
        ]