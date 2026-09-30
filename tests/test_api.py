from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qna():
    response = client.post(
        "/api/qna",
        json={
            "question": "What is Python?",
            "context": "",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "source" in data


def test_explain():
    response = client.post(
        "/api/explain",
        json={
            "topic": "Machine Learning",
            "level": "beginner",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert data["topic"] == "Machine Learning"


def test_summarize():
    response = client.post(
        "/api/summarize",
        json={
            "text": "Artificial intelligence is used in many different fields.",
            "length": "short",
        },
    )

    assert response.status_code == 200
    assert "summary" in response.json()


def test_quiz():
    response = client.post(
        "/api/quiz",
        json={
            "topic": "Data Structures",
            "difficulty": "medium",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "quiz" in data
    assert len(data["quiz"]) == 3


def test_recommendations():
    response = client.get(
        "/api/learn/recommendations?topic=Data%20Analytics"
    )

    assert response.status_code == 200
    data = response.json()

    assert "recommendations" in data
    assert len(data["recommendations"]) == 3