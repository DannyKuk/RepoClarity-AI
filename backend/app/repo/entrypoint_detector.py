from pathlib import Path


def detect_entrypoints(repo_path: str, framework: str | None = None):
    """
    Detect likely application entrypoints.
    Uses lightweight structural heuristics only.
    """

    repo = Path(repo_path)
    entrypoints = []

    if framework == "unity":

        scenes = list((repo / "Assets").rglob("*.unity"))

        for scene in scenes[:3]:  # limit results
            entrypoints.append(str(scene.relative_to(repo)))

    elif framework == "nuxt":

        for candidate in [
            repo / "pages/index.vue",
            repo / "app.vue",
        ]:
            if candidate.exists():
                entrypoints.append(str(candidate.relative_to(repo)))

    elif framework == "fastapi":

        for candidate in [
            repo / "main.py",
            repo / "app/main.py",
        ]:
            if candidate.exists():
                entrypoints.append(str(candidate.relative_to(repo)))

    # --- generic fallback ---
    else:

        common = [
            "main.py",
            "app.py",
            "index.js",
            "main.ts",
        ]

        for name in common:
            candidate = repo / name
            if candidate.exists():
                entrypoints.append(name)

    return entrypoints
