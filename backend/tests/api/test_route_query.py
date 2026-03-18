from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app


# ---------- fakes ----------

class FakeVectorStore:
    def __init__(self):
        self.framework = "python"
        self.entrypoints = ["main.py"]


class FakeVectorStoreCls:
    @staticmethod
    def load(path):
        return FakeVectorStore()


class FakeQueryEngine:
    def answer(self, question, vector_store, model=None):
        return "answer", ["file1.py", "file2.py"]


class FakeRegistry:
    def __init__(self, base_dir: Path):
        self._path = "/repo/path"
        self.index_dir = base_dir

    def get(self, name):
        return self._path

    def index_exists(self, repo):
        return self._exists


class FakeServices:
    def __init__(self, tmp_path):
        self.registry = FakeRegistry(tmp_path)
        self.vector_store_cls = FakeVectorStoreCls()
        self.query_engine = FakeQueryEngine()


class FailingQueryEngine:
    def answer(self, *args, **kwargs):
        raise Exception("boom")


class FailingServices(FakeServices):
    def __init__(self, tmp_path):
        super().__init__(tmp_path)
        self.query_engine = FailingQueryEngine()


# ---------- tests ----------

def test_ask_success(tmp_path):
    repo_name = "testrepo"

    # create fake index dir
    index_dir = tmp_path / repo_name
    index_dir.mkdir()

    services = FakeServices(tmp_path)
    app.state.services = services

    client = TestClient(app)

    response = client.post(
        "/query/ask",
        json={"repo": repo_name, "question": "what is this?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "answer"
    assert data["sources"] == ["file1.py", "file2.py"]
    assert data["framework"] == "python"
    assert data["entrypoints"] == ["main.py"]


def test_ask_repo_not_registered(tmp_path):
    class NoRepoRegistry:
        def get(self, name):
            return None

        index_dir = tmp_path

    class Services:
        registry = NoRepoRegistry()

    app.state.services = Services()

    client = TestClient(app)

    response = client.post(
        "/query/ask",
        json={"repo": "missing", "question": "x"}
    )

    assert response.status_code == 404
    assert "not registered" in response.json()["detail"].lower()


def test_ask_index_not_found(tmp_path):
    repo_name = "testrepo"

    class Registry:
        def get(self, name):
            return "/repo"

        index_dir = tmp_path  # but no folder created

    class Services:
        registry = Registry()

    app.state.services = Services()

    client = TestClient(app)

    response = client.post(
        "/query/ask",
        json={"repo": repo_name, "question": "x"}
    )

    assert response.status_code == 404
    assert "index not found" in response.json()["detail"].lower()


def test_ask_internal_error(tmp_path):
    repo_name = "testrepo"

    index_dir = tmp_path / repo_name
    index_dir.mkdir()

    app.state.services = FailingServices(tmp_path)

    client = TestClient(app)

    response = client.post(
        "/query/ask",
        json={"repo": repo_name, "question": "x"}
    )

    assert response.status_code == 500
    assert "failed to answer" in response.json()["detail"].lower()
