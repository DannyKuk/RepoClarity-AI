from pathlib import Path

# File types that are likely to contain useful code or documentation
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".vue",
    ".md",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".cs",
    ".kt",
    ".java",
    ".swift",
    ".gradle",
    ".xml",
    ".toml",
    ".ini",
    ".env",
    ".shader",
    ".cginc",
}

# Directories that almost always contain generated files,
# build artifacts, IDE metadata, or cache data.
IGNORED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    ".nuxt",
    ".output",
    ".cache",
    "coverage",
    "logs",
    "Library",  # Unity generated
    "Logs",  # Unity logs
    "obj",  # build artifacts
    "bin",
    ".idea",  # JetBrains IDE
    ".vs",  # Visual Studio
    ".vscode",
    ".gradle",
    ".utmp",
    "Temp",
    "UserSettings",
    "MemoryCaptures",
    "Build",
    "Builds",
    "test-v1_BackUpThisFolder_ButDontShipItWithYourGame",

    # Unity example / tutorial folders
    "Examples",
    "Examples & Extras",
    "TutorialInfo",
    "Samples",
    "SampleScenes",
}

# Directories that usually contain tests or demonstration code.
LOW_VALUE_DIRS = {
    "tests",
    "test",
    "examples",
    "example",
    "fixtures",
}

# Path fragments that indicate tutorial or sample content
LOW_VALUE_PATH_CONTAINS = {
    "examples",
    "examples & extras",
    "tutorial",
    "samples",
}

# Individual files that should never be indexed
IGNORED_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    ".DS_Store",
    ".vsconfig",
}

# File names containing these fragments are usually IDE / build metadata
IGNORED_NAME_CONTAINS = {
    "workspace",
    "indexlayout",
    "projectsettingsupdater",
    "unitylinkertoeditordata",
    "codemodel",
    "directory-",
    "cache-v2",
}

# Skip extremely large files (often generated configs or assets)
MAX_FILE_SIZE = 1_000_000  # ~1 MB

# Skip extremely small files that rarely contain meaningful context
MIN_FILE_SIZE = 20


def should_ignore(path: Path) -> bool:
    """
    Determine whether a file or directory should be ignored.
    """

    path_str = str(path).lower()
    name = path.name.lower()

    # Ignore if path contains a known junk directory
    if any(part in IGNORED_DIRS for part in path.parts):
        return True

    # Ignore common low-value directories
    if any(part in LOW_VALUE_DIRS for part in path.parts):
        return True

    # Ignore tutorial / example paths
    if any(token in path_str for token in LOW_VALUE_PATH_CONTAINS):
        return True

    # Ignore specific known junk files
    if name in IGNORED_FILES:
        return True

    # Ignore filenames containing metadata indicators
    if any(token in name for token in IGNORED_NAME_CONTAINS):
        return True

    # Ignore minified JS or source maps
    if path_str.endswith(".min.js") or path_str.endswith(".map"):
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

        # Skip ignored paths early
        if should_ignore(file):
            continue

        # Skip non-files
        if not file.is_file():
            continue

        # Only index supported file extensions
        if file.suffix and file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Skip extremely large or tiny files
        size = file.stat().st_size
        if size > MAX_FILE_SIZE or size < MIN_FILE_SIZE:
            continue

        try:
            content = file.read_text(encoding="utf-8")

            # Skip empty files
            if not content.strip():
                continue

            files.append({
                "path": str(file.relative_to(repo)),
                "content": content
            })

        except Exception:
            # Skip binary or unreadable files
            continue

    return files