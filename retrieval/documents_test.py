from langchain_core.documents import Document
from chunks import SchemaClassChunker  # your chunker class
import re

# Load your snf_models.py file as text
with open("schema.py", "r") as f:
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

# Example: print first document
print(documents[1].page_content)
print(documents[1].metadata)


