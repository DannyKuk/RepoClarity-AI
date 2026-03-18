from app.rag.embedder import Embedder


class FakeModel:
    def __init__(self):
        self.encode_called = False

    def encode(self, texts, **kwargs):
        self.encode_called = True
        self.last_args = (texts, kwargs)
        return [[0.1, 0.2]] * len(texts)

    def get_sentence_embedding_dimension(self):
        return 2


def test_embed_basic():
    fake_model = FakeModel()
    e = Embedder(model=fake_model)

    texts = ["hello", "world"]
    result = e.embed(texts, batch_size=32)

    assert fake_model.encode_called
    assert len(result) == 2

    # verify important params
    _, kwargs = fake_model.last_args
    assert kwargs["batch_size"] == 32
    assert kwargs["convert_to_numpy"] is True
    assert kwargs["normalize_embeddings"] is True


def test_embed_empty():
    e = Embedder(model=FakeModel())

    assert e.embed([]) == []
    assert e.embed(None) == []


def test_lazy_model_loading(monkeypatch):
    class DummyModel:
        def encode(self, *args, **kwargs):
            return [[1.0]]

        def get_sentence_embedding_dimension(self):
            return 1

    def fake_constructor(name):
        return DummyModel()

    monkeypatch.setattr(
        "app.rag.embedder.SentenceTransformer",
        fake_constructor
    )

    e = Embedder(model=None)

    # triggers lazy load
    result = e.embed(["test"])

    assert result == [[1.0]]


def test_dimension():
    e = Embedder(model=FakeModel())

    assert e.dimension() == 2
