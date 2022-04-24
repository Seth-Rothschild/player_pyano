import os
import mido

from flask import Flask
from waitress import serve

app = Flask(__name__)

LOCK = False
SONGS_LIST = os.listdir("songs")

output_name = mido.get_output_names()[1]
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
        if hasattr(msg, "velocity"):
            PORT.send(msg.copy(channel=0, velocity=max(msg.velocity//4, 30)))
            pass
        else:
            PORT.send(msg.copy(channel=0))

    LOCK = False


def run(port=3001):
    try:

        print("Serving Backend on Port {}".format(port))
        serve(app, port=port)
    except KeyboardInterrupt:
        print("\nInterrupted!")
    finally:
        for i in range(128):
            PORT.send(mido.Message('note_off', note=i, velocity=127))

        PORT.reset()
        PORT.close()


if __name__ == "__main__":
    run()
