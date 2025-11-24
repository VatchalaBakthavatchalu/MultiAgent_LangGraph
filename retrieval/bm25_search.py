from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
import numpy as np
from retrieval.search import Search


class BM25Search(Search):
    """BM25 keyword-based search implementation"""

    def __init__(self):
        self.documents = []
        self.bm25 = None
        self.tokenized_docs = []

    def build_index(self, documents: List[str]) -> None:
        """Build BM25 index from documents"""
        self.documents = documents
        # Tokenize documents (simple whitespace tokenization)
        self.tokenized_docs = [doc.lower().split() for doc in documents]
        # Create BM25 instance
        self.bm25 = BM25Okapi(self.tokenized_docs)
        print(f"✓ BM25 index built with {len(documents)} documents")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search using BM25 algorithm"""
        if self.bm25 is None:
            raise ValueError("Index not built. Call build_index() first.")

        # Tokenize query
        tokenized_query = query.lower().split()
        # Calculate BM25 scores
        scores = self.bm25.get_scores(tokenized_query)

        # Get top k results
        top_indices = np.argsort(scores)[-k:][::-1]

        return [
            {
                "content": self.documents[idx],
                "score": float(scores[idx]),
                "index": int(idx)
            }
            for idx in top_indices if scores[idx] > 0
        ]


