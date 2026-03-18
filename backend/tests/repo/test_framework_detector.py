from pathlib import Path
from app.repo.framework_detector import detect_framework


def create_file(path: Path, content=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def test_detect_unity(tmp_path):
    (tmp_path / "Assets").mkdir()
    (tmp_path / "ProjectSettings").mkdir()

    assert detect_framework(tmp_path) == "unity"


def test_detect_nuxt(tmp_path):
    create_file(tmp_path / "nuxt.config.ts")

    assert detect_framework(tmp_path) == "nuxt"


def test_detect_nextjs(tmp_path):
    create_file(tmp_path / "next.config.js")

    assert detect_framework(tmp_path) == "nextjs"


def test_detect_django(tmp_path):
    create_file(tmp_path / "manage.py")

    assert detect_framework(tmp_path) == "django"


def test_detect_fastapi(tmp_path):
    create_file(tmp_path / "app.py", content="from fastapi import FastAPI")

    assert detect_framework(tmp_path) == "fastapi"


def test_detect_none(tmp_path):
    assert detect_framework(tmp_path) is None


def test_unity_takes_priority_over_all(tmp_path):
    # unity + nuxt present
    (tmp_path / "Assets").mkdir()
    (tmp_path / "ProjectSettings").mkdir()
    create_file(tmp_path / "nuxt.config.ts")

    assert detect_framework(tmp_path) == "unity"


def test_nuxt_over_nextjs(tmp_path):
    create_file(tmp_path / "nuxt.config.ts")
    create_file(tmp_path / "next.config.js")

    assert detect_framework(tmp_path) == "nuxt"


def test_nextjs_over_django(tmp_path):
    create_file(tmp_path / "next.config.js")
    create_file(tmp_path / "manage.py")

    assert detect_framework(tmp_path) == "nextjs"


def test_django_over_fastapi(tmp_path):
    create_file(tmp_path / "manage.py")
    create_file(tmp_path / "app.py", content="from fastapi import FastAPI")

    assert detect_framework(tmp_path) == "django"


def test_fastapi_ignores_non_utf8_files(tmp_path):
    bad_file = tmp_path / "bad.py"
    bad_file.write_bytes(b"\xff\xfe\x00\x00")  # invalid utf-8

    # should not crash
    assert detect_framework(tmp_path) is None


def test_fastapi_case_insensitive(tmp_path):
    create_file(tmp_path / "app.py", content="FASTAPI app here")

    assert detect_framework(tmp_path) == "fastapi"
