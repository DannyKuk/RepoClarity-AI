import pytest
import tempfile
from app.rag.vector_store import VectorStore


def sample_docs(n):
    return [{"content": f"text {i}", "path": f"file{i}.py"} for i in range(n)]


def sample_embeddings(n, dim):
    return [[float(i)] * dim for i in range(n)]


def test_add_happy_path():
    vs = VectorStore(dimension=3)

    docs = sample_docs(2)
    embeddings = sample_embeddings(2, 3)

    vs.add(embeddings, docs)

    assert len(vs.documents) == 2


def test_add_length_mismatch():
    vs = VectorStore(dimension=3)

    docs = sample_docs(2)
    embeddings = sample_embeddings(1, 3)

    with pytest.raises(ValueError, match="same length"):
        vs.add(embeddings, docs)


def test_add_dimension_mismatch():
    vs = VectorStore(dimension=3)

    docs = sample_docs(2)
    embeddings = sample_embeddings(2, 2)  # wrong dim

    with pytest.raises(ValueError, match="dimension mismatch"):
        vs.add(embeddings, docs)


def test_search_returns_results():
    vs = VectorStore(dimension=2)

    docs = sample_docs(3)
    embeddings = sample_embeddings(3, 2)

    vs.add(embeddings, docs)

    result = vs.search([0.0, 0.0], k=2)

    assert len(result) == 2
    assert all("content" in r for r in result)


def test_search_empty_store():
    vs = VectorStore(dimension=2)

    result = vs.search([0.0, 0.0])

    assert result == []


def test_save_and_load_roundtrip():
    vs = VectorStore(dimension=2)

    docs = sample_docs(2)
    embeddings = sample_embeddings(2, 2)

    vs.add(embeddings, docs)

    vs.framework = "python"
    vs.summary = "test summary"
    vs.entrypoints = ["main.py"]

    with tempfile.TemporaryDirectory() as tmpdir:
        vs.save(tmpdir)

        loaded = VectorStore.load(tmpdir)

        assert loaded.dimension == 2
        assert len(loaded.documents) == 2

        assert loaded.framework == "python"
        assert loaded.summary == "test summary"
        assert loaded.entrypoints == ["main.py"]


def test_load_missing_optional_files():
    vs = VectorStore(dimension=2)

    docs = sample_docs(1)
    embeddings = sample_embeddings(1, 2)

    vs.add(embeddings, docs)

    with tempfile.TemporaryDirectory() as tmpdir:
        vs.save(tmpdir)

        # manually remove optional files
        import os
        os.remove(f"{tmpdir}/framework.txt")
        os.remove(f"{tmpdir}/summary.txt")
        os.remove(f"{tmpdir}/entrypoints.txt")

        loaded = VectorStore.load(tmpdir)

        assert loaded.framework is None or loaded.framework == ""
        assert loaded.summary is None or loaded.summary == ""
        assert loaded.entrypoints == []
