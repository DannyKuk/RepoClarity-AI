import os

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = os.getenv("REPOCLARITY_MODEL", "qwen2.5-coder")


def ask_ollama(prompt: str, model: str | None = None):

    model = model or DEFAULT_MODEL

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    data = response.json()

    if "response" not in data:
        print("Unexpected Ollama response:", data)
        raise RuntimeError("Ollama returned unexpected response")

    return data["response"]