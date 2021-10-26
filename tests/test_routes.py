from fastapi.testclient import TestClient


def test_sig(client: TestClient):
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

    ####################
    # Empty page
    response = client.get("/sig/list?page_num=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Page content limit
    response = client.get("/sig/list?page_size=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1

    ####################
    # Page content limit + number
    response = client.get("/sig/list?page_num=2&page_size=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["nama"] == "Test SIG2"
    assert result[0]["detail"] == "Lainnya Test SIG"
    assert not result[0]["foto"]
    assert result[0]["is_it_interest"]


def test_competition(client: TestClient):
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

    ####################
    # Empty page
    response = client.get("/competition/list?page_num=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Page content limit
    response = client.get("/competition/list?page_size=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1

    ####################
    # Page content limit + number
    response = client.get("/competition/list?page_num=2&page_size=1")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["nama"] == "Kompetisi Balap Siput"
    assert not result[0]["foto"]
    assert result[0]["link"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
