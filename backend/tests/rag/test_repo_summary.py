from app.rag.repo_summary import RepoSummarizer


class FakeLLM:
    def __init__(self):
        self.called = False
        self.last_prompt = None
        self.last_model = None

    def generate(self, prompt, model=None):
        self.called = True
        self.last_prompt = prompt
        self.last_model = model
        return "summary"


def test_summarize_happy_path():
    files = [
        {"path": "README.md", "content": "info"},
        {"path": "main.py", "content": "code"},
    ]

    llm = FakeLLM()
    summarizer = RepoSummarizer(llm)

    result = summarizer.summarize(files)

    assert llm.called
    assert result == "summary"

    # context should include file names
    assert "README.md" in llm.last_prompt
    assert "main.py" in llm.last_prompt


def test_select_important_files_filters_correctly():
    files = [
        {"path": "README.md", "content": ""},
        {"path": "package.json", "content": ""},
        {"path": "nuxt.config.ts", "content": ""},
        {"path": "main.py", "content": ""},
        {"path": "random.txt", "content": ""},
    ]

    summarizer = RepoSummarizer(llm=None)

    important = summarizer._select_important_files(files)

    paths = [f["path"] for f in important]

    assert "README.md" in paths
    assert "package.json" in paths
    assert "nuxt.config.ts" in paths
    assert "main.py" in paths
    assert "random.txt" not in paths


def test_select_important_files_limit_to_5():
    files = [
        {"path": f"README_{i}.md", "content": ""}
        for i in range(10)
    ]

    summarizer = RepoSummarizer(llm=None)

    important = summarizer._select_important_files(files)

    assert len(important) == 5


def test_build_context_truncates_content():
    long_content = "x" * 3000

    files = [
        {"path": "README.md", "content": long_content}
    ]

    summarizer = RepoSummarizer(llm=None)

    context = summarizer._build_context(files)

    assert "x" * 2000 in context
    assert "x" * 2500 not in context


def test_summarize_with_no_important_files():
    files = [
        {"path": "random.txt", "content": "data"}
    ]

    llm = FakeLLM()
    summarizer = RepoSummarizer(llm)

    result = summarizer.summarize(files)

    # still should call LLM with empty context
    assert llm.called
    assert result == "summary"
