from flask import Flask, jsonify
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.post("/remove_background/")
def remove_background():
    return jsonify({"message": "Hello, World!"})
