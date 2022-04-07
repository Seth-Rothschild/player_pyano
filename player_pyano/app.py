from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route("/")
def welcome():
    return "<h1>Hello, World!</h1>"


def run(port=3000):
    print("Serving App on Port {}".format(port))
    serve(app, port=port)


if __name__ == "__main__":
    run()
