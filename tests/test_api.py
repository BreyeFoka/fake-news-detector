import pytest

import app as api


class StubClassifier:
    """Stands in for the BART model: always ranks "Fake" first."""

    def __init__(self):
        self.calls = []

    def __call__(self, text, candidate_labels):
        self.calls.append(text)
        return {"labels": ["Fake", "Real"], "scores": [0.8123, 0.1877]}


@pytest.fixture
def client(monkeypatch):
    stub = StubClassifier()
    monkeypatch.setattr(api, "get_classifier", lambda: stub)
    api.app.config["TESTING"] = True
    with api.app.test_client() as c:
        c.stub = stub
        yield c


def test_clean_text_lowercases_and_strips_numbers_and_punctuation():
    assert api.clean_text("Breaking!! 3 Aliens   LAND, says NASA.") == "breaking aliens land says nasa"
    assert api.clean_text("") == ""


def test_health_check_names_the_model(client):
    body = client.get("/").get_json()
    assert body["status"] == "healthy"
    assert body["model"] == "facebook/bart-large-mnli"


def test_predict_returns_the_top_label_and_confidence(client):
    res = client.post("/predict", json={"headline": "Scientists discover new planet", "text": "NASA announced it."})
    assert res.status_code == 200
    body = res.get_json()
    assert body["prediction"] == "fake"
    assert body["confidence"] == 81.23
    assert client.stub.calls == ["scientists discover new planet nasa announced it"]


@pytest.mark.parametrize(
    "payload",
    [None, {}, {"headline": "", "text": ""}, {"headline": "a 1 2"}],
)
def test_predict_rejects_missing_or_too_short_input(client, payload):
    res = client.post("/predict", json=payload) if payload is not None else client.post("/predict")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_predict_hides_internal_errors(client, monkeypatch):
    def broken():
        raise RuntimeError("model file missing at /secret/path")

    monkeypatch.setattr(api, "get_classifier", broken)
    res = client.post("/predict", json={"headline": "A long enough headline"})
    assert res.status_code == 500
    assert res.get_json() == {"error": "Internal server error"}
