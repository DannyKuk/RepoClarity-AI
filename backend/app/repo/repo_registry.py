import json
from pathlib import Path


class RepoRegistry:
    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or (Path.home() / ".repoclarity")
        self.index_dir = self.base_path / "indexes"
        self.registry_file = self.base_path / "repos.json"

        self._ensure_directories()

    def _ensure_directories(self):
        self.base_path.mkdir(exist_ok=True)
        self.index_dir.mkdir(exist_ok=True)

        if not self.registry_file.exists():
            self.registry_file.write_text("{}")

    def _load(self):
        try:
            return json.loads(self.registry_file.read_text())
        except Exception:
            return {}

    def _save(self, registry):
        self.registry_file.write_text(json.dumps(registry, indent=2))

    def register(self, name: str, path: str):
        registry = self._load()
        registry[name] = path
        self._save(registry)

    def get(self, name: str):
        return self._load().get(name)

    def list(self):
        return self._load()

    def remove(self, name: str) -> bool:
        registry = self._load()

        if name not in registry:
            return False

        del registry[name]
        self._save(registry)

        return True
