from fastapi.testclient import TestClient


def test_list(client: TestClient):
    response = client.get("/student/list")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 3

    first_result = result[0]
    assert first_result == {
        "username": "nama",
        "nama": "Sebuah Nama",
        "jurusan": "ilmu_komputer",
        "foto_diri": None,
        "house_name": "Musical",
        "is_2021": True,
    }


def test_pagination(client: TestClient):
    ####################
    # Empty page
    response = client.get("/student/list?page=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Non-positive page
    response = client.get("/student/list?page=0")
    assert response.status_code == 422

    response = client.get("/student/list?page=-1")
    assert response.status_code == 422


def test_search(client: TestClient):
    ####################
    # Search
    response = client.get("/student/list?name=Nama")
    assert response.status_code == 200

    result = response.json()
    names = [r["nama"] for r in result]
    assert len(names) == 2
    assert "ZzzzzNama" in names
    assert "Sebuah Nama" in names

    ####################
    # Sorting
    response = client.get("/student/list?sort=desc")
    assert response.status_code == 200

    result = response.json()
    assert result[0]["nama"] == "ZzzzzNama"

    ####################
    # Invalid sorting
    response = client.get("/student/list?sort=invalid")
    assert response.status_code == 422


def test_filters(client: TestClient):
    ####################
    # House filter
    response = client.get("/student/list?house=Space")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2
    assert result[0]["house_name"] == "Space"

    ####################
    # Multiple house filter
    response = client.get("/student/list?house=Space&house=Musical")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 3

    ####################
    # Nonexistent house
    response = client.get("/student/list?house=nonexistent")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Major filter
    response = client.get("/student/list?major=sistem_informasi")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 1
    assert result[0]["nama"] == "ZzzzzNama"
    assert result[0]["jurusan"] == "sistem_informasi"

    ####################
    # Invalid major
    response = client.get("/student/list?major=invalid")
    assert response.status_code == 422


def test_student_detail(client: TestClient):
    response = client.get("/student/test")
    assert response.status_code == 200

    result = response.json()
    assert result["nama"] == "Test User"
    assert result["jurusan"] == "ilmu_komputer"
    assert result["ttl"] == "Jakarta, 12 Agustus 1969"
    assert result["hobi"] == "Gabut"
    assert not result["twitter"]
    assert not result["line"]
    assert not result["instagram"]
    assert not result["foto_diri"]
    assert result["video_diri"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert result["house"]["id"] == 1
    assert result["interests"] == ["Python"]
    assert result["message"] == "lulus cum laude amin"

    # 404 Response
    response = client.get("/student/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "No such student found."}

    # Empty interests
    response = client.get("/student/nama")
    assert response.status_code == 200

    result = response.json()
    assert result["interests"] == []
