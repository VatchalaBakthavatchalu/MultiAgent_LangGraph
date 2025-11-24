import chromadb
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from retrieval.chunk.chunks import SchemaClassChunker
from retrieval.document_loaders.documents import get_documents_from_file

chunker = SchemaClassChunker(max_chunk_size=None)
docs = get_documents_from_file("../schema.py", chunker=chunker)

print(docs[0].page_content)
print(docs[0].metadata)


# Generate IDs for each document
ids = [str(i) for i, _ in enumerate(docs)]


client = chromadb.PersistentClient(path="./chroma_langchain_db")


embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(
    collection_name="foo",
    embedding_function=embeddings
)

vector_store.add_documents(documents=docs, ids=ids)


results = vector_store.similarity_search(query="user has admission in facility", k=3)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")