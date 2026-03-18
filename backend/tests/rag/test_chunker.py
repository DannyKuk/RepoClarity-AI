import pytest

from app.rag.chunker import Chunker


def test_init_valid():
    c = Chunker(chunk_size=100, overlap=20)
    assert c.chunk_size == 100
    assert c.overlap == 20


def test_init_invalid_overlap():
    with pytest.raises(ValueError):
        Chunker(chunk_size=100, overlap=100)


def test_chunk_text_basic():
    c = Chunker(chunk_size=5, overlap=2)
    text = "abcdefghij"  # len = 10

    chunks = c.chunk_text(text)

    # step = 3 → expected starts: 0, 3, 6, 9
    assert chunks == ["abcde", "defgh", "ghij", "j"]


def test_chunk_text_overlap_behavior():
    c = Chunker(chunk_size=5, overlap=2)
    text = "abcdefgh"

    chunks = c.chunk_text(text)

    # overlap check: "abcde" and "defgh" share "de"
    assert chunks[0][-2:] == chunks[1][:2]


def test_chunk_text_empty():
    c = Chunker()
    assert c.chunk_text("") == []


def test_chunk_text_smaller_than_chunk_size():
    c = Chunker(chunk_size=10, overlap=2)
    text = "abc"

    chunks = c.chunk_text(text)

    assert chunks == ["abc"]


def test_chunk_file_basic():
    c = Chunker(chunk_size=5, overlap=2)
    file_dict = {
        "content": "abcdefghij",
        "path": "test.txt"
    }

    result = c.chunk_file(file_dict)

    assert all("content" in r and "path" in r for r in result)
    assert all(r["path"] == "test.txt" for r in result)


def test_chunk_file_missing_keys():
    c = Chunker()

    with pytest.raises(KeyError):
        c.chunk_file({"content": "abc"})  # missing path
