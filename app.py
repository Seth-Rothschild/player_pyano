from flask import Flask, render_template, request, redirect, send_from_directory
import mido
import os
import math
import time

app = Flask(__name__)
CONTEXT = {
    "files": os.listdir("static/midi_files"),
    "selected_file": "",
    "stop": False,
    "paused": False,
    "velocity": 40,
    "song_length": 0,
    "percent_done": 0,
    "playlist": [],
    "DEBUG": False,
}


@app.route("/")
def index():
    context = CONTEXT
    return render_template("index.html", title="Home", context=context)


@app.route("/_app/<path:path>")
def send_app_files(path):
    return send_from_directory("templates/_app", path)


@app.route("/api/play", methods=["POST"])
def play():
    filename = request.json["file"]
    filepath = "static/midi_files/" + filename
    play_midi_file(filepath)
    return "OK", 200


@app.route("/api/volume", methods=["POST"])
def volume():
    if not "volume" in request.json:
        return "Bad Request", 400

    velocity = request.json["volume"]
    if velocity < 0 or velocity > 100:
        return "Bad Request", 400

    CONTEXT["velocity"] = int(velocity)
    return "OK", 200


@app.route("/api/stop", methods=["POST"])
def stop():
    CONTEXT["paused"] = False
    CONTEXT["stop"] = True
    return "OK", 200


@app.route("/api/pause", methods=["POST"])
def pause():
    CONTEXT["paused"] = not CONTEXT["paused"]
    return "OK", 200


@app.route("/api/context", methods=["GET"])
def get_context():
    return CONTEXT


@app.route("/api/playlist/add", methods=["POST"])
def add_to_playlist():
    if not "file" in request.json:
        return "Bad Request", 400
    filename = request.json["file"]
    CONTEXT["playlist"].append(filename)
    return "OK", 200


@app.route("/api/playlist/remove", methods=["POST"])
def remove_from_playlist():
    if not "file" in request.json:
        return "Bad Request", 400
    filename = request.json["file"]
    CONTEXT["playlist"] = [x for x in CONTEXT["playlist"] if x != filename]
    return "OK", 200


@app.route("/api/playlist/duplicate", methods=["POST"])
def duplicate_in_playlist():
    if not "file" in request.json:
        return "Bad Request", 400
    filename = request.json["file"]
    index = CONTEXT["playlist"].index(filename)
    if index == -1:
        return "Bad Request", 400
    CONTEXT["playlist"].insert(index + 1, filename)
    return "OK", 200


@app.route("/api/files/rename", methods=["POST"])
def rename_file():
    if not "file" in request.json or not "newname" in request.json:
        return "Bad Request", 400
    filename = request.json["file"]
    newname = request.json["newname"]
    os.rename("static/midi_files/" + filename, "static/midi_files/" + newname)
    CONTEXT["files"] = os.listdir("static/midi_files")
    return "OK", 200


@app.route("/api/files/delete", methods=["POST"])
def delete_file():
    if not "file" in request.json:
        return "Bad Request", 400
    filename = request.json["file"]
    os.remove("static/midi_files/" + filename)
    CONTEXT["files"] = os.listdir("static/midi_files")
    return "OK", 200


@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    if not "files" in request.files:
        return "Bad Request", 400
    files = request.files.getlist("files")
    for file in files:
        basename = os.path.basename(file.filename)
        file.save("static/midi_files/" + basename)
    CONTEXT["files"] = os.listdir("static/midi_files")
    return "OK", 200

@app.route("/api/files/analytics", methods=["POST"])
def get_file_analytics():
    if not "file" in request.json:
        return "Bad Request", 400
    filename = request.json["file"]
    result = get_midi_analytics(filename)
    return result, 200



def play_midi_file(filepath):
    if not CONTEXT["selected_file"] == "":
        """If a file is already playing, stop it"""
        CONTEXT["stop"] = True
        time.sleep(2)
        cleanup_context()
    try:
        output_name = mido.get_output_names()[1]
        output = mido.open_output(output_name)
    except ModuleNotFoundError:
        print("No output found, using empty output")
        CONTEXT["DEBUG"] = True

    if CONTEXT["DEBUG"]:
        output = empty_output()

    CONTEXT["selected_file"] = filepath
    mid = mido.MidiFile(filepath)
    CONTEXT["song_length"] = mid.length
    previous_time = time.time()
    time_elapsed = 0
    for i, msg in enumerate(mid.play()):
        time_elapsed += time.time() - previous_time
        previous_time = time.time()
        if CONTEXT["song_length"] > 0:
            CONTEXT["percent_done"] = time_elapsed / CONTEXT["song_length"] * 100
        else:
            CONTEXT["percent_done"] = None
        while CONTEXT["paused"]:
            previous_time = time.time()
            if CONTEXT["stop"]:
                break
            pass
        if CONTEXT["stop"]:
            break
        if msg.type == "note_on":
            msg.velocity = math.floor(CONTEXT["velocity"] / 100 * msg.velocity)
        msg.channel = 0

        output.send(msg)
    cleanup_context()
    cleanup_midi(output)
    output.close()

    next_song = play_next()
    if next_song is not None:
        play_midi_file("static/midi_files/" + next_song)


class empty_output:
    def send(self, msg):
        print(msg)
        return msg

    def close(self):
        pass


def cleanup_context():
    CONTEXT["selected_file"] = ""
    CONTEXT["stop"] = False
    CONTEXT["paused"] = False
    CONTEXT["percent_done"] = 0
    CONTEXT["song_length"] = 0


def cleanup_midi(output):
    # turn off all notes, send 3 times
    for _ in range(3):
        for i in range(128):
            output.send(mido.Message("note_off", channel=0, note=i, velocity=0))

    # send control change 123 to turn off all notes
    output.send(mido.Message("control_change", channel=0, control=123, value=0))

    # turn off all pedals
    for i in range(64, 70):
        output.send(mido.Message("control_change", channel=0, control=i, value=0))


def play_next():
    if len(CONTEXT["playlist"]) == 0:
        return
    next_song = CONTEXT["playlist"].pop(0)
    return next_song

def get_midi_analytics(midi_file_path):
    mid = mido.MidiFile("static/midi_files/"+midi_file_path)
    result = {
        "total_notes": 0,
        "total_time": 0,
        "average_note_length": 0,
        "average_velocity": 0,
        "max_velocity": 0,
        "min_velocity": 127,
        "tracks": [],
        "instruments": [],
        "key_signatures": [],
        "time_signature": "",
        "tempo": 0,
    }
    for track in mid.tracks:
        for msg in track:
            if msg.is_meta:
                if msg.type == "track_name":
                    result["tracks"].append(msg.name)
                if msg.type == "device_name":
                    result["instruments"].append(msg.name)
                if msg.type == "key_signature":
                    if msg.key not in result["key_signatures"]:
                        result["key_signatures"].append(msg.key)
                if msg.type == "time_signature":
                    result["time_signature"] = "{}/{}".format(msg.numerator, msg.denominator)
                if msg.type == "set_tempo":
                    result["tempo"] = round(mido.tempo2bpm(msg.tempo))
            if msg.type == "note_on" and msg.velocity > 0:
                result["total_notes"] += 1
                result["average_velocity"] += msg.velocity
                if msg.velocity > result["max_velocity"]:
                    result["max_velocity"] = msg.velocity
                if msg.velocity < result["min_velocity"]:
                    result["min_velocity"] = msg.velocity
                result["total_time"] += msg.time
    if mid.length:
        result["total_time"] = round(mid.length, 2)

    result["average_velocity"] = round(result["average_velocity"] / result["total_notes"], 2)
    result["average_note_length"] = round(result["total_time"] / result["total_notes"], 2)

    return result



if __name__ == "__main__":
    app.run(host="::", debug=True)
