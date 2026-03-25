import pytest
from app.rag.retriever import Retriever


class FakeEmbedder:
    def __init__(self, output):
        self.output = output
        self.called = False

    def embed(self, texts):
        self.called = True
        self.last_texts = texts
        return self.output


class FakeVectorStore:
    def __init__(self):
        self.called = False
        self.last_embedding = None
        self.last_k = None

    def search_hybrid(self, query, query_embedding, k=5):
        self.called = True
        self.last_embedding = query_embedding
        self.last_k = k
        return self._results()

    def search(self, query_embedding, k=5):
        self.called = True
        self.last_embedding = query_embedding
        self.last_k = k
        return self._results()

    def _results(self):
        return [
            {
                "content": "test",
                "metadata": {"path": "test.py", "start": 0, "end": 10},
            }
        ]


def test_retrieve_happy_path():
    embedder = FakeEmbedder([[0.1, 0.2]])
    vector_store = FakeVectorStore()

    r = Retriever(embedder)

    result = r.retrieve("hello", vector_store, k=3)

    assert embedder.called

    rewritten = embedder.last_texts[0]

    assert "hello" in rewritten
    assert "implemented" in rewritten

    assert vector_store.called
    assert vector_store.last_embedding == [0.1, 0.2]
    assert vector_store.last_k == 6

    assert isinstance(result, list)
    assert len(result) > 0

    doc = result[0]

    assert "content" in doc
    assert "metadata" in doc
    assert doc["metadata"]["path"] == "test.py"


def test_retrieve_empty_embedding_raises():
    embedder = FakeEmbedder([])  # no embeddings returned
    vector_store = FakeVectorStore()

    r = Retriever(embedder)

    with pytest.raises(IndexError):
        r.retrieve("hello", vector_store)
