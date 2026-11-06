from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Student API" in data["message"]
    assert "endpoints" in data


def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_single_student_valid():
    response = client.get("/students/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Aniket Kumar"


def test_get_single_student_not_found():
    response = client.get("/students/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_students_search_filter():
    response = client.get("/students?search=Priya")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Priya Sharma"


def test_get_students_min_marks():
    response = client.get("/students?min_marks=90")
    assert response.status_code == 200
    data = response.json()
    for student in data:
        assert student["marks"] >= 90


def test_get_student_report():
    response = client.get("/students/1/report")
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == "A+"
    assert data["status"] == "Passed"


def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "average_marks" in data
    assert "highest_scorer" in data
