import pytest
from app.rag.indexing_service import IndexingService


class FakeVectorStore:
    def __init__(self, dim):
        self.dim = dim
        self.add_called = False
        self.embeddings = None
        self.chunks = None

    def add(self, embeddings, chunks):
        self.add_called = True
        self.embeddings = embeddings
        self.chunks = chunks


class FakeEmbedder:
    def embed(self, texts):
        return [[1.0]] * len(texts)

    def dimension(self):
        return 1


class FakeSummary:
    def summarize(self, files):
        return "summary"


def test_build_index_happy_path():
    scanner = lambda path: [{"content": "hello world", "path": "a.py"}]
    chunker = lambda file: [{"content": file["content"], "path": file["path"]}]
    embedder = FakeEmbedder()
    vector_store_cls = FakeVectorStore
    repo_summary = FakeSummary()
    framework_detector = lambda path: "python"
    file_prioritizer = lambda path, fw: 2
    entrypoint_detector = lambda path, fw: ["main.py"]

    service = IndexingService(
        scanner,
        chunker,
        embedder,
        vector_store_cls,
        repo_summary,
        framework_detector,
        file_prioritizer,
        entrypoint_detector,
    )

    vs = service.build_index("repo")

    assert vs.add_called
    assert vs.framework == "python"
    assert vs.entrypoints == ["main.py"]
    assert vs.summary == "summary"

    # weight = 2 → duplicated chunks
    assert len(vs.chunks) == 2
    assert len(vs.embeddings) == 2


def test_no_files_raises():
    service = IndexingService(
        scanner=lambda _: [],
        chunker=lambda _: [],
        embedder=FakeEmbedder(),
        vector_store_cls=FakeVectorStore,
        repo_summary=FakeSummary(),
        framework_detector=lambda _: "x",
        file_prioritizer=lambda p, f: 1,
        entrypoint_detector=lambda p, f: [],
    )

    with pytest.raises(RuntimeError, match="No files found"):
        service.build_index("repo")


def test_no_chunks_raises():
    scanner = lambda _: [{"content": "x", "path": "a"}]
    chunker = lambda _: []  # nothing produced

    service = IndexingService(
        scanner,
        chunker,
        embedder=FakeEmbedder(),
        vector_store_cls=FakeVectorStore,
        repo_summary=FakeSummary(),
        framework_detector=lambda _: "x",
        file_prioritizer=lambda p, f: 1,
        entrypoint_detector=lambda p, f: [],
    )

    with pytest.raises(RuntimeError, match="No chunks generated"):
        service.build_index("repo")


def test_empty_chunks_filtered_before_embedding():
    scanner = lambda _: [{"content": "x", "path": "a"}]

    chunker = lambda _: [
        {"content": "valid", "path": "a"},
        {"content": "   ", "path": "a"},  # should be removed
    ]

    embedder = FakeEmbedder()

    vector_store_cls = FakeVectorStore

    service = IndexingService(
        scanner,
        chunker,
        embedder,
        vector_store_cls,
        repo_summary=FakeSummary(),
        framework_detector=lambda _: "x",
        file_prioritizer=lambda p, f: 1,
        entrypoint_detector=lambda p, f: [],
    )

    vs = service.build_index("repo")

    # only 1 valid chunk should remain
    assert len(vs.chunks) == 1
    assert vs.chunks[0]["content"] == "valid"


def test_weight_zero_drops_chunks():
    scanner = lambda _: [{"content": "x", "path": "a"}]
    chunker = lambda _: [{"content": "x", "path": "a"}]

    service = IndexingService(
        scanner,
        chunker,
        embedder=FakeEmbedder(),
        vector_store_cls=FakeVectorStore,
        repo_summary=FakeSummary(),
        framework_detector=lambda _: "x",
        file_prioritizer=lambda p, f: 0,  # critical case
        entrypoint_detector=lambda p, f: [],
    )

    with pytest.raises(RuntimeError, match="No chunks generated"):
        service.build_index("repo")
