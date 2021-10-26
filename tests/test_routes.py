from fastapi.testclient import TestClient


def test_student_list(client: TestClient):
    response = client.get("/student/list")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 3

    ####################
    # Empty page
    response = client.get("/student/list?page=2")
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 0

    ####################
    # Search
    response = client.get("/student/list?search_name=Nama")
    assert response.status_code == 200

    result = response.json()
    names = [r["nama"] for r in result]
    assert len(names) == 2
    assert "ZzzzzNama" in names
    assert "Sebuah Nama" in names


def test_student_detail(client: TestClient):
    response = client.get("/student/210684283")
    assert response.status_code == 200

    result = response.json()
    assert result["nama"] == "Test User"
    assert result["jurusan"] == "ilmu_komputer"
    assert result["ttl"] == "Jakarta, 12 Agustus 1969"
    assert result["hobi"] == "Gabut"
    assert not result["twitter"]
    assert not result["line"]
    assert not result["instagram"]
    assert not result["karya"]
    assert not result["foto_diri"]
    assert result["video_diri"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert result["house"]["id"] == 1

    # 404 Response
    response = client.get("/student/1")
    assert response.status_code == 404
