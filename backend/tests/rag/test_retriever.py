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

    def search(self, embedding, k=5):
        self.called = True
        self.last_embedding = embedding
        self.last_k = k
        return ["result"]


def test_retrieve_happy_path():
    embedder = FakeEmbedder([[0.1, 0.2]])
    vector_store = FakeVectorStore()

    r = Retriever(embedder)

    result = r.retrieve("hello", vector_store, k=3)

    assert embedder.called
    assert embedder.last_texts == ["hello"]

    assert vector_store.called
    assert vector_store.last_embedding == [0.1, 0.2]
    assert vector_store.last_k == 3

    assert result == ["result"]


def test_retrieve_empty_embedding_raises():
    embedder = FakeEmbedder([])  # no embeddings returned
    vector_store = FakeVectorStore()

    r = Retriever(embedder)

    with pytest.raises(IndexError):
        r.retrieve("hello", vector_store)
