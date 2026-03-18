from pathlib import Path


class EntrypointDetector:
    def detect(self, repo_path: str, framework: str | None = None):
        repo = Path(repo_path)
        entrypoints = []

        def add_if_exists(path: Path):
            if path.exists():
                entrypoints.append(str(path.relative_to(repo)))

        if framework == "unity":
            scenes = list((repo / "Assets").rglob("*.unity"))
            return [str(s.relative_to(repo)) for s in scenes[:3]]

        framework_map = {
            "nuxt": [
                repo / "pages/index.vue",
                repo / "app.vue",
            ],
            "fastapi": [
                repo / "main.py",
                repo / "app/main.py",
            ],
        }

        if framework in framework_map:
            for candidate in framework_map[framework]:
                add_if_exists(candidate)
            return entrypoints

        for name in ["main.py", "app.py", "index.js", "main.ts"]:
            add_if_exists(repo / name)

        return entrypoints
