from fastapi.testclient import TestClient


def test_home(client: TestClient):
    response = client.get("/")
    assert response.json() == {"message": "Hello world!"}
