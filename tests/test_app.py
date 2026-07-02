from copy import deepcopy

import pytest
from fastapi.testclient import TestClient
from src.app import activities, app


BASE_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(BASE_ACTIVITIES)
    yield
    activities.clear()
    activities.update(original_activities)


client = TestClient(app)


def test_unregister_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_state = client.get("/activities").json()
    assert email not in activities_state[activity_name]["participants"]
