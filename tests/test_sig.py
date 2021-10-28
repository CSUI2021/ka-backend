from fastapi.testclient import TestClient


def test_listing(client: TestClient):
    response = client.get("/sig/list")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2

    assert result[0]["nama"] == "Test SIG"
    assert result[0]["detail"] == "Sebuah Test SIG"
    assert result[0]["foto"] == "https://google.com"
    assert not result[0]["is_it_interest"]

    assert result[1]["nama"] == "Test SIG2"
    assert result[1]["detail"] == "Lainnya Test SIG"
    assert not result[1]["foto"]
    assert result[1]["is_it_interest"]


def test_pagination(client: TestClient):
    ####################
    # Empty page
    response = client.get("/sig/list?page=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Page content limit
    response = client.get("/sig/list?limit=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1

    ####################
    # Page content limit + number
    response = client.get("/sig/list?page=2&limit=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["nama"] == "Test SIG2"
    assert result[0]["detail"] == "Lainnya Test SIG"
    assert not result[0]["foto"]
    assert result[0]["is_it_interest"]
