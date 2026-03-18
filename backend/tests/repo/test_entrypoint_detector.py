from pathlib import Path

from app.repo.entrypoint_detector import EntrypointDetector


def create_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("test")


def to_paths(result):
    return [Path(p) for p in result]


def test_unity_detects_scenes_limit_3(tmp_path):
    detector = EntrypointDetector()

    # create 5 unity scenes
    for i in range(5):
        create_file(tmp_path / "Assets" / f"scene{i}.unity")

    result = detector.detect(tmp_path, framework="unity")

    assert len(result) == 3
    assert all(str(p).endswith(".unity") for p in result)


def test_nuxt_framework_detection(tmp_path):
    detector = EntrypointDetector()

    create_file(tmp_path / "pages" / "index.vue")
    create_file(tmp_path / "app.vue")

    result = detector.detect(tmp_path, framework="nuxt")
    result_paths = to_paths(result)

    assert Path("pages/index.vue") in result_paths
    assert Path("app.vue") in result_paths


def test_fastapi_framework_detection(tmp_path):
    detector = EntrypointDetector()

    create_file(tmp_path / "main.py")
    create_file(tmp_path / "app" / "main.py")

    result = detector.detect(tmp_path, framework="fastapi")
    result_paths = to_paths(result)

    assert Path("main.py") in result_paths
    assert Path("app/main.py") in result_paths


def test_fallback_detection(tmp_path):
    detector = EntrypointDetector()

    create_file(tmp_path / "main.py")
    create_file(tmp_path / "index.js")

    result = detector.detect(tmp_path)
    result_paths = to_paths(result)

    assert Path("main.py") in result_paths
    assert Path("index.js") in result_paths


def test_missing_files_returns_empty(tmp_path):
    detector = EntrypointDetector()

    result = detector.detect(tmp_path)

    assert result == []


def test_paths_are_relative(tmp_path):
    detector = EntrypointDetector()

    create_file(tmp_path / "main.py")

    result = detector.detect(tmp_path)

    # ensure relative paths
    result_paths = to_paths(result)
    assert result_paths == [Path("main.py")]
