from fastapi.testclient import TestClient


def test_listing(client: TestClient):
    response = client.get("/story/list")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2

    assert result[0]["title"] == "Test Story"
    assert result[0]["detail"] == "Yes"
    assert result[0]["foto"] == ["https://google.com"]

    assert result[1]["title"] == "Test Story 2"
    assert result[1]["detail"] == "Electric Boogaloo"
    assert not result[1]["foto"]


def test_pagination(client: TestClient):
    ####################
    # Empty page
    response = client.get("/story/list?page=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Page content limit
    response = client.get("/story/list?limit=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1

    ####################
    # Page content limit + number
    response = client.get("/story/list?page=2&limit=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["title"] == "Test Story 2"
    assert result[0]["detail"] == "Electric Boogaloo"
    assert not result[0]["foto"]
