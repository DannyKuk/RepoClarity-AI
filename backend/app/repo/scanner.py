from pathlib import Path

from app.core.config import ScannerConfig


class RepositoryScanner:
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

    def scan(self, repo_path: str):
        repo = Path(repo_path)

        if not repo.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")

        files = []

        for file in repo.rglob("*"):
            if self.should_ignore(file):
                continue

            if not file.is_file():
                continue

            if file.suffix and file.suffix.lower() not in self.config.supported_extensions:
                continue

            size = file.stat().st_size
            if size > self.config.max_file_size or size < self.config.min_file_size:
                continue

            try:
                content = file.read_text(encoding="utf-8")

                if not content.strip():
                    continue

                files.append({
                    "path": str(file.relative_to(repo)),
                    "content": content,
                })

            except Exception:
                continue

        return files
