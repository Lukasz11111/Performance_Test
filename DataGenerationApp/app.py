from flask import Flask

app = Flask(__name__)

@app.route("/err")
def err():
    raise "You shall not pass!"
    return "<p>Hello, World!</p>"


@app.route("/")
def handle():
    return "<p>Hello, World!</p>"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"







