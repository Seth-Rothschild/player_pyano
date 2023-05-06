import os
from app import app, CONTEXT, play_next, get_midi_analytics


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


def test_duplicate_in_playlist():
    with app.test_client() as client:
        response = client.post("/api/playlist/add", json={"file": "test_song.mid"})
        assert response.status_code == 200

        response = client.post("/api/playlist/add", json={"file": "test_song2.mid"})
        assert response.status_code == 200

        # Duplicate first song twice so it plays 3 times in order
        response = client.post(
            "/api/playlist/duplicate", json={"file": "test_song.mid"}
        )
        response = client.post(
            "/api/playlist/duplicate", json={"file": "test_song.mid"}
        )
        assert response.status_code == 200

        response = client.get("/api/context")
        context = response.json
        assert context["playlist"] == [
            "test_song.mid",
            "test_song.mid",
            "test_song.mid",
            "test_song2.mid",
        ]


def test_get_analytics():
    sample_file = os.listdir("static/midi_files")[0]
    with app.test_client() as client:
        response = client.post("/api/files/analytics", json={})
        assert response.status_code == 400
    with app.test_client() as client:
        response = client.post("/api/files/analytics", json={"file": sample_file})
        assert response.status_code == 200
        assert response.json == get_midi_analytics(sample_file)


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


def test_update_filename():
    with app.test_client() as client:
        sample_file = os.listdir("static/midi_files")[0]
        response = client.post(
            "/api/files/rename",
            json={"file": sample_file, "newname": sample_file + "_1"},
        )
        assert response.status_code == 200
        assert os.path.exists("static/midi_files/" + sample_file + "_1")
        response = client.post(
            "/api/files/rename",
            json={"file": sample_file + "_1", "newname": sample_file},
        )


def test_delete_file():
    with app.test_client() as client:
        sample_file = os.listdir("static/midi_files")[0]
        newfilename = sample_file + "_1"
        with open("static/midi_files/" + sample_file, "rb") as f:
            with open("static/midi_files/" + newfilename, "wb") as f2:
                f2.write(f.read())

        response = client.post("/api/files/delete", json={"file": newfilename})
        assert response.status_code == 200
        assert not os.path.exists("static/midi_files/" + newfilename)


def test_upload_file():
    with app.test_client() as client:
        sample_file = os.listdir("static/midi_files")[0]
        with open("static/midi_files/" + sample_file, "rb") as f:
            response = client.post("/api/files/upload", data={"files": [f]})
            assert response.status_code == 200
            assert os.path.exists("static/midi_files/" + sample_file)


def test_get_midi_analytics():
    for file in os.listdir("static/midi_files"):
        if file.endswith(".mid"):
            sample_file = file
            result = get_midi_analytics(sample_file)
            assert "total_notes" in result
            assert "total_time" in result
            assert "average_note_length" in result
            assert "average_velocity" in result
            assert "max_velocity" in result
            assert "min_velocity" in result
            assert "tracks" in result
            assert "instruments" in result
            assert "key_signatures" in result
            assert "time_signature" in result
            assert "tempo" in result
