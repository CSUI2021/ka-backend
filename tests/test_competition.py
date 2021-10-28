from fastapi.testclient import TestClient


def test_listing(client: TestClient):
    response = client.get("/competition/list")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2

    assert result[0]["nama"] == "Kompetisi Ternak Lele"
    assert not result[0]["foto"]
    assert result[0]["link"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    assert result[1]["nama"] == "Kompetisi Balap Siput"
    assert not result[1]["foto"]
    assert result[1]["link"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_pagination(client: TestClient):
    ####################
    # Empty page
    response = client.get("/competition/list?page=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Page content limit
    response = client.get("/competition/list?limit=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1

    ####################
    # Page content limit + number
    response = client.get("/competition/list?page=2&limit=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["nama"] == "Kompetisi Balap Siput"
    assert not result[0]["foto"]
    assert result[0]["link"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
