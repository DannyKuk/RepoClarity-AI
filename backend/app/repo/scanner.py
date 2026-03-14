from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".vue",
    ".md",
    ".yaml",
    ".yml",
    ".html",
    ".css"
}

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    ".nuxt",
    ".output",
    ".next",
    ".cache"
}

IGNORED_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml"
}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""

    # ignore directories like node_modules, dist, etc.
    if any(part in IGNORED_DIRS for part in path.parts):
        return True

    # ignore specific files
    if path.name in IGNORED_FILES:
        return True

    return False


def scan_repository(repo_path: str):
    """
    Scan repository and return readable files.

    Returns:
        list[dict]: [{"path": str, "content": str}]
    """

    repo = Path(repo_path)

    if not repo.exists():
        raise ValueError(f"Repository path does not exist: {repo_path}")

    files = []

    for file in repo.rglob("*"):

        if should_ignore(file):
            continue

        if file.suffix not in SUPPORTED_EXTENSIONS:
            continue

        if not file.is_file():
            continue

        try:
            content = file.read_text(encoding="utf-8")

            files.append({
                "path": str(file.relative_to(repo)),
                "content": content
            })

        except Exception:
            # Skip binary or unreadable files
            continue

    return files