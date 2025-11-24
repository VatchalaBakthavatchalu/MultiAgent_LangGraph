from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Search(ABC):
    """Abstract base class for search implementations (BM25, semantic, etc.)"""

    @abstractmethod
    def build_index(self, documents: List[str]) -> None:
        """
        Build/index the documents for searching.
        This method prepares the search structure (tokenization, embeddings, etc).

        Args:
            documents: List of text documents to index
        """
        pass

    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search the indexed documents for a query.
        Returns list of results with score and content.

        Args:
            query: Search query string
            k: Number of top results to return

        Returns:
            List of dicts with 'content', 'score', and 'index' keys
        """
        pass