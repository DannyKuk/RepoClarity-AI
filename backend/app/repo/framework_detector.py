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
    SKIP_DIRS = {"venv", ".venv", "node_modules", ".git", "dist", "build", "__pycache__"}
    MAX_FILES = 50
    MAX_CHARS = 2000

    for name in ["main.py", "app.py"]:
        candidate = repo / name
        if candidate.exists():
            try:
                text = candidate.read_text(encoding="utf-8")[:MAX_CHARS]
                if "fastapi" in text.lower():
                    return True
            except Exception:
                pass

    # fallback scan
    count = 0

    for file in repo.rglob("*.py"):
        if any(part in SKIP_DIRS for part in file.parts):
            continue

        if count >= MAX_FILES:
            break

        count += 1

        try:
            text = file.read_text(encoding="utf-8")[:MAX_CHARS]
        except Exception:
            continue

        if "fastapi" in text.lower():
            return True

    return False
