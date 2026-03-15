from pathlib import Path


def detect_framework(repo_path: str) -> str | None:
    """
    Detect the main framework used in the repository.
    """

    repo = Path(repo_path)

    # --- Unity ---
    if (repo / "Assets").exists() and (repo / "ProjectSettings").exists():
        return "unity"

    # --- Nuxt ---
    if (repo / "nuxt.config.ts").exists() or (repo / "nuxt.config.js").exists():
        return "nuxt"

    # --- Next.js ---
    if (repo / "next.config.js").exists():
        return "nextjs"

    # --- FastAPI ---
    for file in repo.rglob("*.py"):
        try:
            text = file.read_text(encoding="utf-8")
            if "fastapi" in text.lower():
                return "fastapi"
        except Exception:
            continue

    # --- Django ---
    if (repo / "manage.py").exists():
        return "django"

    return None
