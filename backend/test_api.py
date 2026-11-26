"""API-boundary tests: authentication, role-scoped access, and action rules."""
import pytest
from starlette.testclient import TestClient

from main import app
from seed import seed

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_demo_data():
    seed()  # drops and recreates the throwaway test database
    yield


def login(username, password="demo123"):
    r = client.post("/login", json={"username": username, "password": password})
    return r


def auth(username):
    return {"Authorization": "Bearer " + login(username).json()["token"]}


def act(username, app_id, action, reason=""):
    return client.post(f"/applications/{app_id}/action", headers=auth(username),
                       json={"action": action, "reason": reason})


# Seed layout: 1,2 submitted; 3,4,5 field verification (Suresh);
# 6 RI review (Meena); 7,8 final decision (Rao).

def test_wrong_password_is_401():
    assert login("suresh", "nope").status_code == 401


def test_unknown_user_is_401():
    assert login("nobody").status_code == 401


def test_queue_requires_a_token():
    assert client.get("/applications").status_code in (401, 403)


def test_queue_is_scoped_to_the_role():
    ids = lambda u: {a["id"] for a in client.get("/applications", headers=auth(u)).json()}
    assert ids("suresh") == {1, 2, 3, 4, 5}
    assert ids("meena") == {6}
    assert ids("rao") == {7, 8}


def test_queue_orders_by_time_at_current_stage():
    days = [a["stage_entered_at"] for a in client.get("/applications", headers=auth("suresh")).json()]
    assert days == sorted(days)


def test_officer_cannot_read_a_case_that_is_not_theirs():
    # Case 1 is still in intake: Meena and Rao have never touched it.
    assert client.get("/applications/1", headers=auth("meena")).status_code == 403
    assert client.get("/applications/1", headers=auth("rao")).status_code == 403


def test_officer_can_read_a_case_at_their_stage_and_one_they_handled():
    assert client.get("/applications/7", headers=auth("rao")).status_code == 200
    # Suresh forwarded case 7 earlier, so he may still read its history.
    assert client.get("/applications/7", headers=auth("suresh")).status_code == 200


def test_wrong_role_action_is_403_and_changes_nothing():
    r = act("meena", 3, "forward")  # case 3 is in field verification, not Meena's stage
    assert r.status_code == 403
    detail = client.get("/applications/3", headers=auth("suresh")).json()
    assert detail["application"]["status"] == "field_verification"


def test_return_and_reject_need_a_reason_on_the_server():
    assert act("suresh", 3, "return", "   ").status_code == 422
    assert act("suresh", 3, "reject", "").status_code == 422


def test_valid_action_moves_the_case_and_records_history():
    assert act("suresh", 3, "forward", "visit done").status_code == 200
    detail = client.get("/applications/3", headers=auth("suresh")).json()
    assert detail["application"]["status"] == "ri_review"
    assert detail["history"][-1]["reason"] == "visit done"
    # it left Suresh's queue and entered Meena's
    assert 3 not in {a["id"] for a in client.get("/applications", headers=auth("suresh")).json()}
    assert 3 in {a["id"] for a in client.get("/applications", headers=auth("meena")).json()}


def test_ai_use_is_recorded_in_history():
    client.post("/applications/3/action", headers=auth("suresh"),
                json={"action": "forward", "reason": "ok", "ai_reason_use": "edited"})
    detail = client.get("/applications/3", headers=auth("suresh")).json()
    assert detail["history"][-1]["ai_reason_use"] == "edited"


def test_assist_is_refused_for_a_case_at_another_stage():
    assert client.post("/applications/7/assist", headers=auth("suresh")).status_code == 403


def test_assist_returns_rule_flags_even_without_an_llm(monkeypatch):
    monkeypatch.setattr("main.llm_assist", lambda *a, **k: None)
    r = client.post("/applications/2/assist?lang=en", headers=auth("suresh")).json()
    assert any("Ration card" in f for f in r["flags"])
    assert r["summary"] == ""
