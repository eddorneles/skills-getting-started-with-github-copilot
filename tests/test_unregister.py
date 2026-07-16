from src import app as app_module


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    activity = app_module.activities["Chess Club"]
    email_to_unregister = "daniel@mergington.edu"

    assert email_to_unregister in activity["participants"]

    # Act
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={email_to_unregister}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == (
        f"Unregistered {email_to_unregister} from Chess Club"
    )

    get_response = client.get("/activities")
    activities = get_response.json()
    assert email_to_unregister not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_error(client):
    # Arrange
    unused_email = "ghost@mergington.edu"
    activity = app_module.activities["Chess Club"]

    assert unused_email not in activity["participants"]

    # Act
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={unused_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
