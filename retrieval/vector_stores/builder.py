# retrieval/vectorstore/builder.py

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from retrieval.chunk.chunks import SchemaClassChunker
from retrieval.document_loaders.documents import get_documents_from_file


def build_vector_store():
    chunker = SchemaClassChunker(max_chunk_size=None)
    docs = get_documents_from_file("../schema.py", chunker=chunker)

    ids = [str(i) for i, _ in enumerate(docs)]

    client = chromadb.PersistentClient(path="./chroma_langchain_db")

    embeddings = HuggingFaceEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        client=client,
        collection_name="foo",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db"
    )

    vector_store.add_documents(documents=docs, ids=ids)
    print("✅ Vector store built & documents added.")

