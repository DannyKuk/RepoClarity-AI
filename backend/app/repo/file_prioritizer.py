from pathlib import Path


def get_file_weight(path: str, framework: str | None = None) -> int:
    path_lower = path.lower()
    parts = Path(path_lower).parts

    weight = 1

    if "readme" in path_lower:
        return 4

    if path_lower.endswith("package.json"):
        return 3

    if "config" in path_lower:
        weight = max(weight, 2)

    framework_rules = {
        "unity": [
            (lambda p, parts: "scripts" in parts, 4),
            (lambda p, parts: "ui" in parts, 3),
        ],
        "nuxt": [
            (lambda p, parts: "pages" in parts, 4),
            (lambda p, parts: "components" in parts, 3),
            (lambda p, parts: "layouts" in parts, 3),
        ],
        "fastapi": [
            (lambda p, parts: "routers" in parts, 3),
            (lambda p, parts: p.endswith("main.py"), 4),
        ],
    }

    for condition, value in framework_rules.get(framework, []):
        if condition(path_lower, parts):
            weight = max(weight, value)

    return weight