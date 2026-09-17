from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_sectors_and_desk():
    sectors = client.get("/api/sectors")
    assert sectors.status_code == 200
    assert sectors.json()["sectors"]
    desk = client.get("/api/desk/GC")
    assert desk.status_code == 200
    payload = desk.json()
    assert payload["product"]["code"] == "GC"
    assert payload["oracle"] is None


def test_unknown_product():
    response = client.get("/api/desk/NOT_A_REAL_CODE")
    assert response.status_code == 404


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "financeAnalyze" in response.text
