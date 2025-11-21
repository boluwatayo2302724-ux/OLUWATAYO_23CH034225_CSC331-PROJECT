# LLM_QA_CLI.py
import os
import requests
import re
import string
import json

# Google Gemini API - Free tier (no credit card, 1k req/day)
API_KEY = os.getenv("GEMINI_API_KEY")  # Set in env or input below
if not API_KEY:
    API_KEY = input("Enter your Google Gemini API key: ").strip()

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
MODEL = "gemini-1.5-flash"  # Free, fast model


def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenization (simple split) & remove extra whitespace
    tokens = text.split()
    processed = ' '.join(tokens).strip()
    return processed


def ask_llm(question):
    processed = preprocess_text(question)
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
        response = requests.post(URL, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {e} (Check key/internet)"


print("LLM Q&A System (CLI) - Type 'quit' to exit\n")
while True:
    question = input("Ask a question: ").strip()
    if question.lower() in ["quit", "exit", "bye"]:
        print("Goodbye!")
        break
    if not question:
        print("Please enter a valid question.\n")
        continue

    print(f"\nOriginal: {question}")
    processed = preprocess_text(question)
    print(f"Processed: {processed}")
    print("Thinking...")

    answer = ask_llm(question)
    print(f"\nAnswer:\n{answer}\n{'-' * 50}\n")