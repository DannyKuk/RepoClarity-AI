import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder"


def ask_ollama(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    data = response.json()

    # debug fallback if API response changes
    if "response" not in data:
        print("Unexpected Ollama response:", data)
        raise RuntimeError("Ollama returned unexpected response")

    return data["response"]