import requests
import os


class LMStudioClient:
    def __init__(
            self,
            base_url: str = "http://localhost:1234",
            default_model: str | None = None,
            timeout: int = 120,
    ):
        self.base_url = base_url.rstrip("/")
        self.endpoint_chat = f"{self.base_url}/v1/chat/completions"
        self.endpoint_models = f"{self.base_url}/v1/models"
        self.default_model = default_model or os.getenv(
            "REPOCLARITY_MODEL", "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF"
        )
        self.timeout = timeout

    def generate(self, prompt: str, model: str | None = None) -> str:
        model = model or self.default_model

        try:
            response = requests.post(
                self.endpoint_chat,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"LM Studio request failed: {exc}") from exc

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Invalid JSON response from LM Studio")

        if "choices" not in data or not data["choices"]:
            raise RuntimeError(f"Unexpected LM Studio response: {data}")

        return data["choices"][0]["message"]["content"]

    def list_models(self):
        try:
            response = requests.get(self.endpoint_models, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"LM Studio list models failed: {exc}") from exc
        
        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Invalid JSON response from LM Studio")

        if "data" not in data:
            raise RuntimeError(f"Unexpected LM Studio models response: {data}")

        models = [model["id"] for model in data["data"]]
        return models
