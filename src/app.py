# src/app.py
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
