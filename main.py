from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

summarizer = pipeline("summarization", model="t5-small")

@app.route("/")
def home():
    return "ShortPress Summarizer is running!"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    summary = summarizer(text, max_length=60, min_length=10, do_sample=False)[0]['summary_text']
    return jsonify({"summary": summary})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
