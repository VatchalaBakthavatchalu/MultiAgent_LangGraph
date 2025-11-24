from retrieval.search.bm25_search import BM25Search

# Sample documents
"""documents = [
    "Machine learning is a subset of artificial intelligence",
    "Python is a popular programming language for data science",
    "Neural networks are inspired by biological neurons",
    "Deep learning uses multiple layers of neural networks",
    "Natural language processing helps computers understand text",
    "Transformers have revolutionized NLP and computer vision",
    "Artificial intelligence is transforming industries worldwide"
]"""

from langchain_core.documents import Document
from retrieval.chunk.chunks import SchemaClassChunker  # your chunker class
import re

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


print("=" * 70)
print("BM25 SEARCH EXAMPLE")
print("=" * 70)

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




