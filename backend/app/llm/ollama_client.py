import subprocess
import requests
import os


class OllamaClient:
    def __init__(
            self,
            base_url: str = "http://localhost:11434",
            default_model: str | None = None,
            timeout: int = 120,
    ):
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/api/generate"
        self.default_model = default_model or os.getenv(
            "REPOCLARITY_MODEL", "qwen2.5-coder"
        )
        self.timeout = timeout

    def generate(self, prompt: str, model: str | None = None) -> str:
        model = model or self.default_model

        try:
            response = requests.post(
                self.endpoint,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Invalid JSON response from Ollama")

        if "response" not in data:
            raise RuntimeError(f"Unexpected Ollama response: {data}")

        return data["response"]

    def list_models(self):
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            raise RuntimeError("Ollama not found in PATH")
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"Ollama list failed: {exc}") from exc

        lines = result.stdout.strip().split("\n")

        # skip header
        models = []
        for line in lines[1:]:
            parts = line.split()
            if parts:
                models.append(parts[0])

        return models
