from bm25_search import BM25Search
from semantic_search import SemanticSearch


# Sample documents
documents = [
    "Machine learning is a subset of artificial intelligence",
    "Python is a popular programming language for data science",
    "Neural networks are inspired by biological neurons",
    "Deep learning uses multiple layers of neural networks",
    "Natural language processing helps computers understand text",
    "Transformers have revolutionized NLP and computer vision",
    "Artificial intelligence is transforming industries worldwide"
]

print("=" * 70)
print("BM25 SEARCH EXAMPLE")
print("=" * 70)

# Initialize and build BM25 index
bm25_search = BM25Search()
bm25_search.build_index(documents)

# Search with BM25
query = "machine learning neural networks"
print(f"\nQuery: '{query}'")
print("\nTop 3 Results (BM25):")
results = bm25_search.search(query, k=3)
for i, result in enumerate(results, 1):
    print(f"\n  {i}. Score: {result['score']:.4f}")
    print(f"     Content: {result['content']}")




