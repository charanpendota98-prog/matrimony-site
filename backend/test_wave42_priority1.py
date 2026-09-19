"""W42 Priority-1: recent profiles, similar profiles, manual ID verification."""
import os
import sys
os.environ.setdefault("TSAP_AUTH_MODE", "off")
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient  # noqa: E402
import hardening  # noqa: E402
import main  # noqa: E402


def _user(tsap_id, name, gender="Bride", age=25, caste="Reddy", district="Hyderabad", approved=True):
    return {
        "tsap_id": tsap_id, "full_name": name, "gender": gender, "age": age,
        "caste": caste, "district": district, "state": "TS", "job": "Software",
        "education": "BTech", "marital_status": "Pelli Kaledu", "is_approved": approved,
        "is_banned": False, "photo_urls": [], "created_at": "2026-09-19T10:00:00",
    }


def setup_function():
    main.DB_USERS[:] = [
        _user("RED001", "Target"), _user("RED002", "Closest", age=26),
        _user("KAM001", "Other", age=31, caste="Kamma", district="Guntur"),
        _user("GRO001", "Viewer", gender="Groom", age=28),
    ]
    main.DB_VIEWS[:] = [{"tsap_id": "RED001", "viewer_id": "GRO001", "at": "2026-09-19T10:00:00"}]


def test_similar_profiles_rank_closest_first():
    data = TestClient(main.app).get("/api/profiles/RED001/similar").json()
    assert data["profiles"][0]["tsap_id"] == "RED002"
    assert data["profiles"][0]["similarity_score"] > data["profiles"][1]["similarity_score"]


def test_recently_viewed_is_private_and_deduplicated():
    client = TestClient(main.app)
    response = client.get("/api/recently-viewed/GRO001")
    assert response.status_code == 200
    assert [p["tsap_id"] for p in response.json()["profiles"]] == ["RED001"]
    assert "phone" not in response.json()["profiles"][0]


def test_admin_can_set_and_revoke_id_badge(monkeypatch):
    monkeypatch.setattr(main.DBSTORE, "save", lambda *args, **kwargs: True)
    monkeypatch.setattr(main.MAUD, "audit", lambda *args, **kwargs: None)
    client = TestClient(main.app)
    headers = {"X-Admin-Key": hardening.ADMIN_KEY}
    enabled = client.post("/api/admin/profiles/RED001/id-verification", headers=headers,
                          json={"verified": True, "method": "government_id", "note": "manual match"})
    assert enabled.status_code == 200 and enabled.json()["id_verified"] is True
    assert client.get("/api/search/RED001").json()["profile"]["id_verified"] is True
    disabled = client.post("/api/admin/profiles/RED001/id-verification", headers=headers,
                           json={"verified": False, "method": "manual_review"})
    assert disabled.status_code == 200 and disabled.json()["id_verified"] is False
