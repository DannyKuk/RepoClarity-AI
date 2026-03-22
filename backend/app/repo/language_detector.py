from pathlib import Path
from app.core.config import ScannerConfig


EXTENSION_MAP = {
    ".py": "python",
    ".ts": "typescript",
    ".js": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".cs": "csharp",
}


class LanguageDetector:
    def __init__(self, config: ScannerConfig | None = None):
        self.config = config or ScannerConfig()

    def should_ignore(self, path: Path) -> bool:
        path_str = str(path).lower()
        name = path.name.lower()

        if any(part in self.config.ignored_dirs for part in path.parts):
            return True

        if any(part in self.config.low_value_dirs for part in path.parts):
            return True

        if any(token in path_str for token in self.config.low_value_path_contains):
            return True

        if name in self.config.ignored_files:
            return True

        if any(token in name for token in self.config.ignored_name_contains):
            return True

        if path_str.endswith(".min.js") or path_str.endswith(".map"):
            return True

        return False

    def detect(self, repo_path) -> list[str]:
        repo = Path(repo_path)

        counts = {}

        for file in repo.rglob("*"):
            relative = file.relative_to(repo)

            if self.should_ignore(relative):
                continue

            if not file.is_file():
                continue

            ext = file.suffix.lower()

            if ext not in self.config.supported_extensions:
                continue

            if ext not in EXTENSION_MAP:
                continue

            try:
                size = file.stat().st_size
            except Exception:
                continue

            if size < self.config.min_file_size or size > self.config.max_file_size:
                continue

            lang = EXTENSION_MAP[ext]
            counts[lang] = counts.get(lang, 0) + size

        return sorted(counts, key=counts.get, reverse=True)