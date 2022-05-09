import json
from urllib import response
from flask import Flask, render_template, request, jsonify
from chat import feedback

app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("index.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    response = feedback(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
