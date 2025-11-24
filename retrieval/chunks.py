import re
from abc import ABC, abstractmethod
from typing import List, Optional

class Chunker(ABC):
    """Abstract base class for all chunker implementations.

       All chunker classes should inherit from this base class and implement
       the chunk method.
       """

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        """Split text into chunks.

        Args:
            text (str): The text to chunk

        Returns:
            List[str]: List of text chunks
        """
        pass


class SchemaClassChunker(Chunker):
    """
    Chunk Python ORM schemas by class definition.

    It extracts:
    - class name
    - docstring
    - class body (columns + relationships)
    """

    CLASS_PATTERN = re.compile(
        r"(class\s+\w+\(Base\):[\s\S]*?)(?=\nclass\s+\w+\(Base\):|\Z)",
        re.MULTILINE,
    )

    def __init__(self, max_chunk_size: Optional[int] = None):
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str) -> List[str]:
        matches = self.CLASS_PATTERN.findall(text)
        chunks = []

        for block in matches:
            clean_block = block.strip()

            if self.max_chunk_size and len(clean_block) > self.max_chunk_size:
                chunks.extend(self._split_large_block(clean_block))
            else:
                chunks.append(clean_block)

        return chunks

    def _split_large_block(self, block: str) -> List[str]:
        """Further chunk large classes by method/column groups."""
        sub_chunks = []

        parts = re.split(r"\n\s{4}(?=#|\w)", block)  # split inside class body
        header = parts[0]  # class signature + docstring
        remainder = parts[1:] if len(parts) > 1 else []

        running = [header]

        for part in remainder:
            if sum(len(x) for x in running) + len(part) > self.max_chunk_size:
                sub_chunks.append("\n".join(running))
                running = [header, part]
            else:
                running.append(part)

        if running:
            sub_chunks.append("\n".join(running))

        return sub_chunks
