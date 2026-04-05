import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the activities state antes de cada teste, usando o nome da atividade
    initial_participants = {
        "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
        "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
        "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"],
        "Basketball Team": [],
        "Soccer Team": [],
        "Art Club": [],
        "Music Club": [],
        "Debate Club": [],
        "Science Club": [],
    }
    for name, activity in activities.items():
        activity["participants"] = list(initial_participants.get(name, []))


def test_list_activities():
    # Arrange
    # (Nada extra, pois o estado já está resetado)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Art Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_prevent_duplicate_signup():
    # Arrange
    email = "uniqueuser@mergington.edu"
    activity = "Programming Class"
    # Act
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"].lower()


def test_remove_participant():
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_participant():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
