import pytest
from app.llm.ollama_client import OllamaClient


# ---------- generate ----------

def test_generate_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"response": "hello"}

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("requests.post", fake_post)

    client = OllamaClient()

    result = client.generate("test prompt")

    assert result == "hello"


def test_generate_request_failure(monkeypatch):
    import requests

    def fake_post(*args, **kwargs):
        raise requests.exceptions.RequestException("fail")

    monkeypatch.setattr("requests.post", fake_post)

    client = OllamaClient()

    with pytest.raises(RuntimeError, match="Ollama request failed"):
        client.generate("test")


def test_generate_invalid_json(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError()

    monkeypatch.setattr("requests.post", lambda *a, **k: FakeResponse())

    client = OllamaClient()

    with pytest.raises(RuntimeError, match="Invalid JSON"):
        client.generate("test")


def test_generate_missing_response_key(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"not_response": "oops"}

    monkeypatch.setattr("requests.post", lambda *a, **k: FakeResponse())

    client = OllamaClient()

    with pytest.raises(RuntimeError, match="Unexpected Ollama response"):
        client.generate("test")


def test_generate_uses_custom_model(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"response": "ok"}

    def fake_post(url, json, timeout):
        captured["model"] = json["model"]
        return FakeResponse()

    monkeypatch.setattr("requests.post", fake_post)

    client = OllamaClient(default_model="default-model")

    client.generate("test", model="custom-model")

    assert captured["model"] == "custom-model"


# ---------- list_models ----------

def test_list_models_success(monkeypatch):
    class FakeResult:
        stdout = "NAME SIZE\nmodel1 1GB\nmodel2 2GB\n"

    def fake_run(*args, **kwargs):
        return FakeResult()

    monkeypatch.setattr("subprocess.run", fake_run)

    client = OllamaClient()

    result = client.list_models()

    assert result == ["model1", "model2"]


def test_list_models_not_found(monkeypatch):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr("subprocess.run", fake_run)

    client = OllamaClient()

    with pytest.raises(RuntimeError, match="Ollama not found"):
        client.list_models()


def test_list_models_failure(monkeypatch):
    import subprocess

    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "ollama")

    monkeypatch.setattr("subprocess.run", fake_run)

    client = OllamaClient()

    with pytest.raises(RuntimeError, match="Ollama list failed"):
        client.list_models()
