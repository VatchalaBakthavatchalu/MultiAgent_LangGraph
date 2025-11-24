from retrieval.search.semantic_search import SemanticSearch

"""documents = [
    "Machine learning is a subset of artificial intelligence",
    "Python is a popular programming language for data science",
    "Neural networks are inspired by biological neurons",
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


# Initialize with all-MiniLM-L6-v2 directly
semantic_search = SemanticSearch()
semantic_search.build_index(documents)

results = semantic_search.search("user has admission to the facility", k=2)
for result in results:
    print(f"Score: {result['score']:.4f} - {result['content']}")