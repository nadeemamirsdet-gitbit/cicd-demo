import os

from flask import Flask, jsonify, request

app = Flask(__name__)


def add(a: float, b: float) -> float:
    return a + b


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/version")
def version():
    return jsonify(version=os.getenv("APP_VERSION", "dev"))


@app.get("/add")
def add_endpoint():
    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
    except (KeyError, ValueError):
        return jsonify(error="query parameters a and b must be numbers"), 400
    return jsonify(result=add(a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))