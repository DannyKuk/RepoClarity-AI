from pathlib import Path


def detect_framework(repo_path: str) -> str | None:
    repo = Path(repo_path)

    if _is_unity(repo):
        return "unity"

    if _is_nuxt(repo):
        return "nuxt"

    if _is_nextjs(repo):
        return "nextjs"

    if _is_django(repo):
        return "django"

    if _is_fastapi(repo):
        return "fastapi"

    return None


# ---- detectors ----

def _is_unity(repo: Path) -> bool:
    return (repo / "Assets").exists() and (repo / "ProjectSettings").exists()


def _is_nuxt(repo: Path) -> bool:
    return any(
        (repo / name).exists()
        for name in ["nuxt.config.ts", "nuxt.config.js"]
    )


def _is_nextjs(repo: Path) -> bool:
    return (repo / "next.config.js").exists()


def _is_django(repo: Path) -> bool:
    return (repo / "manage.py").exists()


def _is_fastapi(repo: Path) -> bool:
    # limit scan to avoid nuking performance
    for file in repo.rglob("*.py"):
        try:
            text = file.read_text(encoding="utf-8")
        except Exception:
            continue

        if "fastapi" in text.lower():
            return True

    return False
