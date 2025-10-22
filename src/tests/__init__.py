import tests
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]

    # Duplicate sign up should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg.status_code == 200
    assert f"Unregistered {email}" in resp_unreg.json()["message"]

    # Unregister again should fail
    resp_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg2.status_code == 400

def test_signup_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert resp.status_code == 404

def test_unregister_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert resp.status_code == 404