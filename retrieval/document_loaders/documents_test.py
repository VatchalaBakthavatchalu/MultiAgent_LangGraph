from retrieval.chunk.chunks import SchemaClassChunker
from retrieval.document_loaders.documents import get_documents_from_file

chunker = SchemaClassChunker(max_chunk_size=None)
docs = get_documents_from_file("../schema.py", chunker=chunker)

print(docs[0].page_content)
print(docs[0].metadata)
