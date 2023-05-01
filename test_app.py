import os
from app import app, CONTEXT, play_next


def test_index():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_app_files_are_served():
    with app.test_client() as client:
        response = client.get("/_app/version.json")
        assert response.status_code == 200


def test_volume():
    with app.test_client() as client:
        response = client.post("/api/volume", json={"volume": 50})
        assert response.status_code == 200

        response = client.get("/api/context")
        context = response.json
        assert context["velocity"] == 50


def test_volume_bad_input():
    with app.test_client() as client:
        response = client.post("/api/volume", json={})
        assert response.status_code == 400


def test_volume_max_min():
    with app.test_client() as client:
        response = client.post("/api/volume", json={"volume": 101})
        assert response.status_code == 400

        response = client.post("/api/volume", json={"volume": -1})
        assert response.status_code == 400


def test_stop_pause():
    with app.test_client() as client:
        response = client.post("/api/pause")
        assert response.status_code == 200

        response = client.get("/api/context")
        context = response.json
        assert context["paused"] == True

        response = client.post("/api/stop")
        assert response.status_code == 200

        response = client.get("/api/context")
        context = response.json
        assert context["paused"] == False
        assert context["stop"] == True


def test_add_to_playlist():
    with app.test_client() as client:
        response = client.post("/api/playlist/add", json={"file": "test_song.mid"})
        assert response.status_code == 200

        response = client.get("/api/context")
        context = response.json
        assert context["playlist"] == ["test_song.mid"]


def test_remove_from_playlist():
    with app.test_client() as client:
        response = client.post("/api/playlist/add", json={"file": "test_song.mid"})
        assert response.status_code == 200

        response = client.post("/api/playlist/remove", json={"file": "test_song.mid"})
        assert response.status_code == 200

        response = client.get("/api/context")
        context = response.json
        assert context["playlist"] == []


def test_play_next():
    test_data = {
        "playlist": ["test_song2.mid", "test_song3.mid"],
        "selected_file": "test_song1.mid",
    }
    CONTEXT.update(test_data)
    result = play_next()
    assert result == "test_song2.mid"
    assert CONTEXT["playlist"] == ["test_song3.mid"]


def test_playlist_bad_input():
    with app.test_client() as client:
        response = client.post("/api/playlist/add", json={})
        assert response.status_code == 400

        response = client.post("/api/playlist/remove", json={})
        assert response.status_code == 400
