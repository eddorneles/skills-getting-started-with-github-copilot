from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess%20Club/unregister?email=daniel@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"

    get_response = client.get("/activities")
    activities = get_response.json()
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_error():
    response = client.delete("/activities/Chess%20Club/unregister?email=ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
