from flask import Flask, render_template, request, redirect
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


def play_midi_file(filepath):
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
    start_time = time.time()
    for i, msg in enumerate(mid.play()):
        CONTEXT["percent_done"] = (time.time() - start_time) / CONTEXT["song_length"] * 100
        while CONTEXT["paused"]:
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
    # turn off all notes
    for i in range(128):
        output.send(mido.Message("note_off", channel=0, note=i, velocity=0))

    # turn off all pedals
    for i in range(64, 70):
        output.send(mido.Message("control_change", channel=0, control=i, value=0))

@app.route("/play", methods=["POST"])
def play():
    filename = request.form["file"]
    filepath = "static/midi_files/" + filename
    PLAYER = play_midi_file(filepath)
    return redirect("/")


@app.route("/reduce_velocity", methods=["POST"])
def reduce():
    velocity = request.form["velocity"]
    CONTEXT["velocity"] = int(velocity)
    return redirect("/")


@app.route("/stop", methods=["POST"])
def stop():
    CONTEXT["stop"] = True
    return redirect("/")

@app.route("/pause", methods=["POST"])
def pause():
    CONTEXT["paused"] = not CONTEXT["paused"]
    return redirect("/")

@app.route("/get_context", methods=["GET"])
def get_context():
    return CONTEXT


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
