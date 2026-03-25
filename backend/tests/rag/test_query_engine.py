import pytest
from app.rag.query_engine import QueryEngine


class FakeRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.called = False

    def retrieve(self, question, vector_store, k=20):
        self.called = True
        self.last_question = question
        return self.chunks


class FakeLLM:
    def __init__(self):
        self.called = False
        self.last_prompt = None
        self.last_model = None

    def generate(self, prompt, model=None):
        self.called = True
        self.last_prompt = prompt
        self.last_model = model
        return "fake answer"


class FakeVectorStore:
    def __init__(self, framework=None, entrypoints=None, summary=None):
        self.framework = framework
        self.entrypoints = entrypoints or []
        self.summary = summary


def make_chunk(content, path, start=0, end=10):
    return {
        "content": content,
        "metadata": {
            "path": path,
            "start": start,
            "end": end,
        },
    }


def test_answer_happy_path():
    chunks = [
        make_chunk("code1", "a.py"),
        make_chunk("code2", "b.py"),
    ]

    retriever = FakeRetriever(chunks)
    llm = FakeLLM()
    vs = FakeVectorStore("python", ["main.py"], "summary")

    engine = QueryEngine(retriever, llm)

    answer, sources = engine.answer("how does this work?", vs)

    assert retriever.called
    assert llm.called
    assert answer == "fake answer"

    paths = sorted(s["path"] for s in sources)
    assert paths == ["a.py", "b.py"]


def test_overview_question_triggers_overview_prompt():
    chunks = [make_chunk("x", "a.py")]

    retriever = FakeRetriever(chunks)
    llm = FakeLLM()
    vs = FakeVectorStore("python", [], "")

    engine = QueryEngine(retriever, llm)

    engine.answer("What does this project do?", vs)

    assert "high-level question" in llm.last_prompt


def test_detailed_question_triggers_detailed_prompt():
    chunks = [make_chunk("x", "a.py")]

    retriever = FakeRetriever(chunks)
    llm = FakeLLM()
    vs = FakeVectorStore("python", [], "")

    engine = QueryEngine(retriever, llm)

    engine.answer("Where is the database connection?", vs)

    assert "Use the provided information" in llm.last_prompt


def test_context_truncates_content():
    long_text = "x" * 1000
    chunks = [make_chunk(long_text, "a.py")]

    retriever = FakeRetriever(chunks)
    llm = FakeLLM()
    vs = FakeVectorStore()

    engine = QueryEngine(retriever, llm)

    engine.answer("question", vs)

    assert "x" * 800 in llm.last_prompt
    assert "x" * 900 not in llm.last_prompt


def test_sources_are_deduplicated_and_sorted():
    chunks = [
        make_chunk("x", "b.py", 0, 10),
        make_chunk("y", "a.py", 0, 10),
        make_chunk("z", "a.py", 20, 30),
    ]

    retriever = FakeRetriever(chunks)
    llm = FakeLLM()
    vs = FakeVectorStore()

    engine = QueryEngine(retriever, llm)

    _, sources = engine.answer("question", vs)

    paths = sorted(set(s["path"] for s in sources))
    assert paths == ["a.py", "b.py"]


def test_missing_framework_and_summary_defaults():
    chunks = [make_chunk("x", "a.py")]

    retriever = FakeRetriever(chunks)
    llm = FakeLLM()
    vs = FakeVectorStore(framework=None, summary=None)

    engine = QueryEngine(retriever, llm)

    engine.answer("question", vs)

    assert "unknown" in llm.last_prompt


def test_empty_chunks_still_calls_llm():
    retriever = FakeRetriever([])
    llm = FakeLLM()
    vs = FakeVectorStore()

    engine = QueryEngine(retriever, llm)

    answer, sources = engine.answer("question", vs)

    assert llm.called
    assert answer == "fake answer"
    assert sources == []


@pytest.mark.parametrize("question", [
    "What does this project do?",
    "What is this repository?",
    "How does it start?",
])
def test_is_overview_question_true(question):
    engine = QueryEngine(None, None)
    assert engine._is_overview_question(question)


@pytest.mark.parametrize("question", [
    "Where is the API defined?",
    "How is authentication implemented?",
])
def test_is_overview_question_false(question):
    engine = QueryEngine(None, None)
    assert not engine._is_overview_question(question)