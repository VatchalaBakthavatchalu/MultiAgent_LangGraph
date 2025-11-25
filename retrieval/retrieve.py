from retrieval.search.bm25_search import BM25Search
from langchain_core.documents import Document
from retrieval.chunk.chunks import SchemaClassChunker  # your chunker class
import re
from retrieval.vector_stores.retriever import VectorRetriever

# Load your snf_models.py file as text
with open("../schema.py", "r") as f:
    code_text = f.read()

# Initialize the chunker
chunker = SchemaClassChunker(max_chunk_size=None)  # adjust chunk size as needed
chunks = chunker.chunk(code_text)


# Function to extract table name from a class chunk
def extract_table_name(chunk: str) -> str:
    match = re.search(r"class\s+(\w+)\(Base\):", chunk)
    return match.group(1) if match else "Unknown"


# Convert each chunk into a LangChain Document
documents = []

for chunk in chunks:
    table_name = extract_table_name(chunk)

    doc = Document(
        page_content=chunk,
        metadata={
            "table_name": table_name,
            "source": "schema.py",
        },
    )
    documents.append(doc)

# Initialize and build BM25 index
bm25_search = BM25Search()
bm25_search.build_index(documents)

# Search with BM25
query = "user had admission"
result = bm25_search.search(query)
print(f"\nQuery: '{query}'")
print("\nTop 3 Results (BM25):")
results = bm25_search.search(query, k=3)
for i, result in enumerate(results, 1):
    print(f"\n  {i}. Score: {result['score']:.4f}")
    print(f"     Content: {result['content']}")




# IMPORTANT: Use the SAME path + collection that were used when building the vector DB
retriever = VectorRetriever(
    path="./chroma_langchain_db",       # <-- CHANGE THIS IF your DB is elsewhere
    collection="foo"                   # <-- CHANGE THIS to your actual collection name
)


results = retriever.search(query, k=3)

for doc in results:
    print("*", doc.page_content, doc.metadata)


