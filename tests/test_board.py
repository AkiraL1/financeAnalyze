from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_overview_and_board():
    overview = client.get("/api/overview")
    assert overview.status_code == 200
    payload = overview.json()
    assert payload["kpis"]
    assert any(row["code"] == "GC" for row in payload["tape"])
    board = client.get("/api/board")
    assert board.status_code == 200
    assert any(row["code"] == "CL" for row in board.json()["rows"])


def test_intel_and_review_offline():
    intel = client.get("/api/intel")
    assert intel.status_code == 200
    body = intel.json()
    assert body["live"] is False
    assert body["count"] >= 1
    review = client.get("/api/review")
    assert review.status_code == 200
    data = review.json()
    assert "每日简报" in data["markdown"]
    assert data["briefs"]


def test_static_assets_and_shell():
    page = client.get("/")
    assert page.status_code == 200
    assert "关注品种" in page.text
    css = client.get("/static/desk.css")
    assert css.status_code == 200
    js = client.get("/static/app.js")
    assert js.status_code == 200
