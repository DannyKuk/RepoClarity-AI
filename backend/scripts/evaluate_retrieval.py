from app.rag.embedder import Embedder
from app.rag.retriever import Retriever
from app.rag.vector_store import VectorStore


store = VectorStore.load(
    r"C:\Users\danny\.repoclarity\indexes\testing"
)

embedder = Embedder()
retriever = Retriever(embedder)


TEST_CASES = [
    {
        "query": "retriever",
        "expected": ["retriever", "query_engine", "services"],
    },
    {
        "query": "indexing",
        "expected": ["indexing_service", "retriever"],
    },
    {
        "query": "scanner",
        "expected": ["scanner", "indexing_service"],
    },
    {
        "query": "vector store",
        "expected": ["vector_store", "indexing_service"],
    },
    {
        "query": "entrypoint",
        "expected": ["entrypoint", "query_engine"],
    },
    {
        "query": "config",
        "expected": ["config", "settings"],
    },
]


def is_relevant(path: str, expected_keywords):
    path = path.lower()
    return any(keyword in path for keyword in expected_keywords)


def match_score(results, expected_keywords):
    """
    Loose recall-style score:
    - full hit = 1
    - partial semantic-ish match = 0.5
    """
    score = 0

    for doc in results:
        path = doc.get("metadata", {}).get("path", "").lower()

        if is_relevant(path, expected_keywords):
            score += 1

    return score


def precision_at_k(results, expected_keywords, k=3):
    """
    Precision@k = how many of top-k are relevant
    """
    top_k = results[:k]

    hits = sum(
        1 for doc in top_k
        if is_relevant(doc.get("metadata", {}).get("path", ""), expected_keywords)
    )

    return hits / k if k > 0 else 0


def evaluate():
    total_score = 0
    total_possible = 0

    total_precision = 0
    num_cases = 0

    print("\n=== RETRIEVAL EVALUATION ===")

    for case in TEST_CASES:
        query = case["query"]
        expected = case["expected"]

        results = retriever.retrieve(query, store, k=5)

        score = match_score(results, expected)
        precision = precision_at_k(results, expected, k=3)

        total_score += score
        total_possible += len(results)

        total_precision += precision
        num_cases += 1

        print(f"\nQuery: {query}")
        print("Results:")
        for doc in results:
            path = doc.get("metadata", {}).get("path")
            print(f"  - {path}")

        print(f"Score: {score:.1f}/{len(results)}")
        print(f"Precision@3: {precision:.2f}")

    print("\n=== FINAL RESULTS ===")
    print(f"Total Score: {total_score:.1f}/{total_possible}")
    print(f"Avg Precision@3: {(total_precision / num_cases):.2f}")


if __name__ == "__main__":
    evaluate()