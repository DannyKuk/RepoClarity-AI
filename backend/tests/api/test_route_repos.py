from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app


class FakeVectorStore:
    def __init__(self):
        self.framework = "python"

    def save(self, path):
        path.mkdir(parents=True, exist_ok=True)


class FakeVectorStoreCls:
    @staticmethod
    def load(path):
        return FakeVectorStore()


class FakeIndexingService:
    def build_index(self, path):
        return FakeVectorStore()


class FakeRegistry:
    def __init__(self, base_dir: Path):
        self._data = {}
        self.index_dir = base_dir

    def list(self):
        return self._data

    def register(self, name, path):
        self._data[name] = path

    def get(self, name):
        return self._data.get(name)

    def remove(self, name):
        if name in self._data:
            del self._data[name]
            return True
        return False


class FakeServices:
    def __init__(self, tmp_path):
        self.registry = FakeRegistry(tmp_path)
        self.vector_store_cls = FakeVectorStoreCls()
        self.indexing_service = FakeIndexingService()


def test_get_repos_empty(tmp_path):
    app.state.services = FakeServices(tmp_path)
    client = TestClient(app)

    response = client.get("/repos/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_repos_with_framework(tmp_path):
    services = FakeServices(tmp_path)
    services.registry.register("repo1", "/path")

    # create index dir so framework is loaded
    index_dir = tmp_path / "repo1"
    index_dir.mkdir()

    app.state.services = services
    client = TestClient(app)

    response = client.get("/repos/")

    data = response.json()

    assert data[0]["name"] == "repo1"
    assert data[0]["framework"] == "python"


def test_index_repo_success(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    app.state.services = FakeServices(tmp_path)
    client = TestClient(app)

    response = client.post(
        "/repos/index",
        json={"name": "repo1", "path": str(repo_dir)},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "indexed"


def test_index_repo_invalid_path(tmp_path):
    app.state.services = FakeServices(tmp_path)
    client = TestClient(app)

    response = client.post(
        "/repos/index",
        json={"name": "repo1", "path": "does_not_exist"},
    )

    assert response.status_code == 400


def test_index_repo_not_directory(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("x")

    app.state.services = FakeServices(tmp_path)
    client = TestClient(app)

    response = client.post(
        "/repos/index",
        json={"name": "repo1", "path": str(file)},
    )

    assert response.status_code == 400


def test_reindex_success(tmp_path):
    services = FakeServices(tmp_path)
    services.registry.register("repo1", "/repo/path")

    app.state.services = services
    client = TestClient(app)

    response = client.post("/repos/repo1/reindex")

    assert response.status_code == 200
    assert response.json()["status"] == "reindexed"


def test_reindex_not_found(tmp_path):
    app.state.services = FakeServices(tmp_path)
    client = TestClient(app)

    response = client.post("/repos/missing/reindex")

    assert response.status_code == 404


def test_delete_repo_success(tmp_path):
    services = FakeServices(tmp_path)
    services.registry.register("repo1", "/repo/path")

    # create index dir
    index_dir = tmp_path / "repo1"
    index_dir.mkdir()

    app.state.services = services
    client = TestClient(app)

    response = client.delete("/repos/repo1")

    assert response.status_code == 200
    assert response.json()["status"] == "removed"


def test_delete_repo_not_found(tmp_path):
    app.state.services = FakeServices(tmp_path)
    client = TestClient(app)

    response = client.delete("/repos/missing")

    assert response.status_code == 404
