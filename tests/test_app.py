from src.app import activities


class TestGetActivities:
    def test_returns_all_activities_with_expected_fields(self, client):
        # Arrange
        expected_activity = "Chess Club"

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        payload = response.json()
        assert expected_activity in payload
        assert {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }.issubset(payload[expected_activity])


class TestSignup:
    def test_adds_student_to_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "new.student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json() == {
            "message": f"Signed up {email} for {activity_name}"
        }

    def test_rejects_duplicate_student(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "existing.student@mergington.edu"
        activities[activity_name]["participants"].append(email)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_rejects_unknown_activity(self, client):
        # Arrange
        activity_name = "Unknown Club"
        email = "new.student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestRemoveFromActivity:
    def test_removes_student_from_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "student.to.remove@mergington.edu"
        activities[activity_name]["participants"].append(email)

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json() == {
            "message": f"Removed {email} from {activity_name}"
        }

    def test_rejects_removing_unregistered_student(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "not.registered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_rejects_removing_student_from_unknown_activity(self, client):
        # Arrange
        activity_name = "Unknown Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
