from pathlib import Path


class EntrypointDetector:
    def detect(
        self,
        repo_path: str,
        framework: str | None = None,
        languages: list[str] | None = None,
    ):
        repo = Path(repo_path)
        entrypoints = []
        languages = languages or []

        def add_if_exists(path: Path):
            if path.exists():
                entrypoints.append(str(path.relative_to(repo)))

        # --- Framework-specific ---
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
            if entrypoints:
                return entrypoints

        # --- Language-based fallback ---
        candidates = []

        if "python" in languages:
            candidates += ["main.py", "app.py", "server.py"]

        if "javascript" in languages or "typescript" in languages:
            candidates += ["index.js", "index.ts", "server.js", "main.ts"]

        if "go" in languages:
            candidates += ["main.go"]

        if "rust" in languages:
            candidates += ["main.rs"]

        # --- Generic fallback (if no language info) ---
        if not candidates:
            candidates = ["main.py", "app.py", "index.js", "index.ts"]

        # --- Search common locations ---
        search_roots = [
            repo,
            repo / "src",
            repo / "app",
            repo / "backend",
            repo / "cmd",
        ]

        for root in search_roots:
            if not root.exists():
                continue

            for name in candidates:
                path = root / name
                if path.exists():
                    entrypoints.append(str(path.relative_to(repo)))

        # Deduplicate + limit
        seen = set()
        unique = []
        for ep in entrypoints:
            if ep not in seen:
                seen.add(ep)
                unique.append(ep)

        return unique[:5]