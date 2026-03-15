def get_file_weight(path: str, framework: str | None = None) -> int:
    """
    Determine how important a file is for indexing.
    Higher weight means higher retrieval probability.
    """

    path = path.lower()

    weight = 1

    # universal priorities
    if "readme" in path:
        return 4

    if path.endswith("package.json"):
        return 3

    if "config" in path:
        weight = max(weight, 2)

    # framework-specific rules
    if framework == "unity":
        if "/scripts/" in path:
            weight = 4
        elif "/ui/" in path:
            weight = max(weight, 3)

    elif framework == "nuxt":
        if "/pages/" in path:
            weight = 4
        elif "/components/" in path:
            weight = 3
        elif "/layouts/" in path:
            weight = max(weight, 3)

    elif framework == "fastapi":
        if "/routers/" in path:
            weight = 3
        elif path.endswith("main.py"):
            weight = 4

    return weight
