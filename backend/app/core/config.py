from dataclasses import dataclass, field


@dataclass
class ScannerConfig:
    supported_extensions: set[str] = field(default_factory=lambda: {
        ".py", ".js", ".ts", ".vue", ".md", ".yaml", ".yml",
        ".html", ".css", ".cs", ".kt", ".java", ".swift",
        ".gradle", ".xml", ".toml", ".ini", ".env",
        ".shader", ".cginc",
    })

    ignored_dirs: set[str] = field(default_factory=lambda: {
        ".git", "node_modules", "dist", "build", "__pycache__",
        ".venv", ".nuxt", ".output", ".cache", "coverage", "logs",
        "Library", "Logs", "obj", "bin", ".idea", ".vs", ".vscode",
        ".gradle", ".utmp", "Temp", "UserSettings", "MemoryCaptures",
        "Build", "Builds",
        "test-v1_BackUpThisFolder_ButDontShipItWithYourGame",
        "Examples", "Examples & Extras", "TutorialInfo",
        "Samples", "SampleScenes",
    })

    low_value_dirs: set[str] = field(default_factory=lambda: {
        "tests", "test", "examples", "example", "fixtures",
    })

    low_value_path_contains: set[str] = field(default_factory=lambda: {
        "examples", "examples & extras", "tutorial", "samples",
    })

    ignored_files: set[str] = field(default_factory=lambda: {
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        ".DS_Store", ".vsconfig",
    })

    ignored_name_contains: set[str] = field(default_factory=lambda: {
        "workspace", "indexlayout", "projectsettingsupdater",
        "unitylinkertoeditordata", "codemodel",
        "directory-", "cache-v2",
    })

    max_file_size: int = 1_000_000
    min_file_size: int = 20
