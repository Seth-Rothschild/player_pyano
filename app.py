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
    "velocity": 100,
    "song_length": 0,
    "percent_done": 0,
    "DEBUG": False,
}


@app.route("/")
def index():
    context = CONTEXT
    return render_template("index.html", title="Home", context=context)

@app.route('/_app/<path:path>')
def send_report(path):
    return send_from_directory('templates/_app', path)

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


@app.route("/api/play", methods=["POST"])
def play():
    filename = request.json["file"]
    filepath = "static/midi_files/" + filename
    PLAYER = play_midi_file(filepath)
    return redirect("/")


@app.route("/api/volume", methods=["POST"])
def reduce():
    velocity = request.json["volume"]
    CONTEXT["velocity"] = int(velocity)
    return redirect("/")


@app.route("/api/stop", methods=["POST"])
def stop():
    CONTEXT["paused"] = False
    CONTEXT["stop"] = True
    return redirect("/")


@app.route("/api/pause", methods=["POST"])
def pause():
    CONTEXT["paused"] = not CONTEXT["paused"]
    return redirect("/")


@app.route("/api/context", methods=["GET"])
def get_context():
    return CONTEXT


if __name__ == "__main__":
    app.run(host="::1", debug=True)
