import os
import mido

from flask import Flask
from waitress import serve

app = Flask(__name__)

LOCK = False
SONGS_LIST = os.listdir("songs")

output_name = mido.get_output_names()[0]
PORT = mido.open_output(output_name)


@app.route("/")
def welcome():
    return "<h1>Hello, World!</h1>", 200


@app.route("/songs")
def get_songs():
    songs = os.listdir("songs")
    return {"songs_list": SONGS_LIST}, 200


@app.route("/play")
def play():
    global LOCK
    if LOCK:
        return "Please wait.", 425
    else:
        LOCK = True

    if not len(SONGS_LIST):
        return "No songs loaded!", 500
    path = os.path.join("songs", SONGS_LIST[0])
    midi_file = mido.MidiFile(path)
    print("Playing {} ({} Seconds)".format(path, midi_file.length))

    for msg in midi_file.play():
        PORT.send(msg)
    LOCK = False


def run(port=3000):
    try:

        print("Serving App on Port {}".format(port))
        serve(app, port=port)
    except KeyboardInterrupt:
        print("n/Interrupted!")
    finally:
        PORT.reset()
        PORT.close()


if __name__ == "__main__":
    run()
