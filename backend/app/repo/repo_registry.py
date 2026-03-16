import json
from pathlib import Path


REPOCLARITY_HOME = Path.home() / ".repoclarity"
INDEX_DIR = REPOCLARITY_HOME / "indexes"
REGISTRY_FILE = REPOCLARITY_HOME / "repos.json"


def ensure_directories():
    REPOCLARITY_HOME.mkdir(exist_ok=True)
    INDEX_DIR.mkdir(exist_ok=True)

    if not REGISTRY_FILE.exists():
        REGISTRY_FILE.write_text("{}")


def load_registry():
    ensure_directories()

    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def register_repo(name, path):
    registry = load_registry()

    registry[name] = path

    save_registry(registry)


def get_repo(name):
    registry = load_registry()

    return registry.get(name)


def list_repos():
    return load_registry()


def remove_repo(name: str):
    registry = load_registry()

    if name not in registry:
        return False
    del registry[name]

    save_registry(registry)

    return True