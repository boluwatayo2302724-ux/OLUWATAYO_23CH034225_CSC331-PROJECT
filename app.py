# app.py
from flask import Flask, render_template, request
import requests
import os
import re
import string
import json

app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY")
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    processed = ' '.join(tokens).strip()
    return processed


@app.route("/", methods=["GET", "POST"])
def index():
    original = processed = answer = None

    if request.method == "POST":
        original = request.form["question"]
        processed = preprocess_text(original)

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Answer this question concisely: {processed}"
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 1024,
                "temperature": 0.7
            }
        }
        params = {"key": API_KEY}

        try:
            resp = requests.post(URL, json=payload, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            answer = "Sorry, API error. Check your key or internet."

    return render_template("index.html",
                           original=original,
                           processed=processed,
                           answer=answer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))