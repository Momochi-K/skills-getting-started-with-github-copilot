from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    # No special setup required for the root redirect.

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.history[0].status_code == 307
    assert response.history[0].headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Drama Club",
        "Debate Team",
        "Science Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == expected_activity_names
    assert payload["Chess Club"]["participants"][0] == "michael@mergington.edu"


def test_signup_adds_new_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_email(client):
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + duplicate_email)

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_existing_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_rejects_unknown_email(client):
    # Arrange
    unknown_email = "unknown@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup?email=" + unknown_email)

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
