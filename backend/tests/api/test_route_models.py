from fastapi.testclient import TestClient
from app.main import app


class FakeLLM:
    def list_models(self):
        return ["model1", "model2"]


class FakeServices:
    def __init__(self):
        self.llm = FakeLLM()


class FailingLLM:
    def list_models(self):
        raise RuntimeError("boom")


class FailingServices:
    def __init__(self):
        self.llm = FailingLLM()


def test_list_models_success():
    app.state.services = FakeServices()
    client = TestClient(app)

    response = client.get("/models/")

    assert response.status_code == 200
    assert response.json() == {"models": ["model1", "model2"]}


def test_list_models_failure():
    app.state.services = FailingServices()
    client = TestClient(app)

    response = client.get("/models/")

    assert response.status_code == 500
    assert "boom" in response.json()["detail"]
