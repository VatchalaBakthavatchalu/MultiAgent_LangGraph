from retrieval.vector_stores.retriever import VectorRetriever

# IMPORTANT: Use the SAME path + collection that were used when building the vector DB
retriever = VectorRetriever(
    path="./chroma_langchain_db",       # <-- CHANGE THIS IF your DB is elsewhere
    collection="foo"                   # <-- CHANGE THIS to your actual collection name
)

query = "user has admission in facility"
results = retriever.search(query, k=3)

print("Collections:", retriever.client.list_collections())
print("Count:", retriever.vector_store._collection.count())




for doc, score in results:
    print("Score:", score)
    print("Content:", doc.page_content)
    print("---")
