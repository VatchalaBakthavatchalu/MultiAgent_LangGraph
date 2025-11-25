# retrieval/vectorstore/retriever.py

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from retrieval.vector_stores.builder import build_vector_store


class VectorRetriever:
    def __init__(self, path="./chroma_langchain_db", collection="foo"):

        self.client = chromadb.PersistentClient(path=path)

        self.embeddings = HuggingFaceEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            client=self.client,
            collection_name=collection,
            embedding_function=self.embeddings,
            persist_directory=path
        )

        # -------------------------
        # ✅ Check if collection is empty
        # -------------------------
        count = self.vector_store._collection.count()

        if count == 0:
            print("⚠️ Collection is empty. Building vector store...")
            build_vector_store()   # <-- Build and populate DB
            print("✅ Vector store initialized.")
        else:
            print(f"📦 Loaded existing vector store ({count} documents).")

    def search(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(query=query, k=k)
