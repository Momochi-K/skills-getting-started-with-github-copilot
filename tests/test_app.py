import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


def test_unregister_participant_removes_email_from_activity(client):
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_error_for_unknown_email(client):
    response = client.delete("/activities/Chess Club/signup?email=unknown@mergington.edu")

    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
