#!/usr/bin/env python

from flask import Flask
import csv

app = Flask("lisa")


@app.route("/", methods=["GET"])
def hello_world():
    return f"<h1>Hello, world from {app.name}™</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
