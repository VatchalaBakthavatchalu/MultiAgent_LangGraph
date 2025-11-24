import os
import sys
sys.path.append("/")

from retrieval.chunk.chunks import SchemaClassChunker

# Path to the schema file
schema_path = os.path.join(os.path.dirname(__file__), "schema.py")
# Read the schema as TEXT (not as Python module)
with open(schema_path, "r") as f:
    schema_text = f.read()

# Chunk it
chunker = SchemaClassChunker(max_chunk_size=None)
chunks = chunker.chunk(schema_text)

for i, c in enumerate(chunks, 1):
    print(f"--- Chunk {i} ---")
    print(c)
    print()