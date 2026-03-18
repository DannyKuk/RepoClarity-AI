from pathlib import Path
import pytest

from app.repo.scanner import RepositoryScanner
from app.core.config import ScannerConfig

VALID_CONTENT = "this is valid content for scanner testing"


def create_file(path: Path, content: str = VALID_CONTENT):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def create_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    return repo


def test_scan_happy_path(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "main.py")

    scanner = RepositoryScanner(config=ScannerConfig())

    result = scanner.scan(repo)

    assert len(result) == 1
    assert result[0]["path"] == "main.py"


def test_ignores_git_directory(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / ".git" / "file.py")

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_ignores_test_directory(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "tests" / "file.py")

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_ignores_low_value_path_contains(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "examples" / "file.py")

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_ignored_files(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "package-lock.json")

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_supported_extensions(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "file.md")

    scanner = RepositoryScanner(config=ScannerConfig())

    result = scanner.scan(repo)

    assert len(result) == 1
    assert result[0]["path"] == "file.md"


def test_min_file_size_enforced(tmp_path):
    repo = create_repo(tmp_path)

    small_file = repo / "small.py"
    small_file.parent.mkdir(parents=True, exist_ok=True)
    small_file.write_text("short")  # < 20 chars

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_max_file_size_enforced(tmp_path):
    repo = create_repo(tmp_path)

    large_content = "x" * (1_000_001)
    create_file(repo / "large.py", large_content)

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_empty_content_ignored(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "file.py", " " * 50)

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_non_utf8_file_skipped(tmp_path):
    repo = create_repo(tmp_path)

    file = repo / "bad.py"
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_bytes(b"\xff\xfe\x00")

    scanner = RepositoryScanner(config=ScannerConfig())

    assert scanner.scan(repo) == []


def test_relative_paths(tmp_path):
    repo = create_repo(tmp_path)
    create_file(repo / "src" / "file.py")

    scanner = RepositoryScanner(config=ScannerConfig())

    result = scanner.scan(repo)

    assert len(result) == 1
    assert Path(result[0]["path"]) == Path("src/file.py")


def test_nonexistent_path_raises():
    scanner = RepositoryScanner(config=ScannerConfig())

    with pytest.raises(ValueError):
        scanner.scan("does_not_exist")
