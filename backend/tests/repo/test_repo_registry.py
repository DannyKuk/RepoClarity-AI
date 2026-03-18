from app.repo.repo_registry import RepoRegistry


def test_initialization_creates_structure(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    assert (tmp_path / "indexes").exists()
    assert (tmp_path / "repos.json").exists()


def test_register_and_get(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    registry.register("repo1", "/path/to/repo")

    assert registry.get("repo1") == "/path/to/repo"


def test_list_returns_all(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    registry.register("repo1", "/a")
    registry.register("repo2", "/b")

    result = registry.list()

    assert result == {
        "repo1": "/a",
        "repo2": "/b",
    }


def test_remove_existing(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    registry.register("repo1", "/a")

    assert registry.remove("repo1") is True
    assert registry.get("repo1") is None


def test_remove_nonexistent(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    assert registry.remove("missing") is False


def test_register_overwrites_existing(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    registry.register("repo1", "/a")
    registry.register("repo1", "/b")

    assert registry.get("repo1") == "/b"


def test_corrupted_registry_file(tmp_path):
    registry = RepoRegistry(base_path=tmp_path)

    # break the JSON file
    (tmp_path / "repos.json").write_text("not valid json")

    # should not crash
    assert registry.get("anything") is None
    assert registry.list() == {}
