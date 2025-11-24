from langchain_core.documents import Document
from retrieval.chunk.chunks import SchemaClassChunker
import re
from typing import List



def get_documents_from_file(
    file_path: str,
    chunker: SchemaClassChunker = None
) -> List[Document]:
    """
    Reads a Python file and converts class definitions into LangChain Documents.

    Args:
        file_path (str): Path to the Python file containing classes.
        chunker (SchemaClassChunker, optional): Chunker instance.
            If None, a default one is created.

    Returns:
        List[Document]: List of LangChain Document objects.
    """
    # Read file
    with open(file_path, "r") as f:
        code_text = f.read()

    # Initialize chunker if not provided
    if chunker is None:
        chunker = SchemaClassChunker(max_chunk_size=None)

    # Split code into chunks
    chunks = chunker.chunk(code_text)

    # Helper function to extract table/class name
    def extract_table_name(chunk: str) -> str:
        match = re.search(r"class\s+(\w+)\(Base\):", chunk)
        return match.group(1) if match else "Unknown"

    # Convert each chunk into a Document
    documents = [
        Document(
            page_content=chunk,
            metadata={
                "table_name": extract_table_name(chunk),
                "source": file_path,
            },
        )
        for chunk in chunks
    ]

    return documents
