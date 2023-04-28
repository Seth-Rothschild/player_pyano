from flask import Flask, render_template, request, redirect
import mido
import os
import math

app = Flask(__name__)
CONTEXT = {
    "files": os.listdir("static/midi_files"),
    "stop": False,
    "velocity": 100,
}


@app.route("/")
def index():
    context = CONTEXT
    return render_template("index.html", title="Home", context=context)


def play_midi_file(filepath):
    output_name = mido.get_output_names()[1]
    output = mido.open_output(output_name)
    mid = mido.MidiFile(filepath)
    for msg in mid.play():
        if CONTEXT["stop"]:
            break
        if msg.type == "note_on":
            msg.velocity = math.floor(CONTEXT["velocity"] / 100 * msg.velocity)
        output.send(msg)
        print(msg)
    CONTEXT["stop"] = False
    output.close()


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


if __name__ == "__main__":
    app.run(debug=True)
