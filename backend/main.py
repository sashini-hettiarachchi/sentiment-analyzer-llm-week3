from flask import Flask, request, jsonify
import requests
from transformers import pipeline
from dotenv import load_dotenv
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load fine-tuned model from Hugging Face
sentiment_analyzer = pipeline("sentiment-analysis")

# Groq Cloud API for Llama 3
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def llama_prompt(text):
    return f"Classify the sentiment of this text as positive or negative: \"{text}\""

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Sentiment Analysis API!"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    print('data',data)
    text = data.get("text")
    model = data.get("model")
    
    if not text or not model:
        return jsonify({"error": "Missing required parameters."}), 400

    try:
        if model == "custom":
            analysis = sentiment_analyzer(text)
            result = {
                "sentiment": analysis[0]["label"].lower(),
                "confidence": analysis[0]["score"],
            }
        elif model == "llama":
            response = requests.post(
                GROQ_API_URL,
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "system", "content": llama_prompt(text)}],
                },
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            )
            print('response',response)
            output = response.json()["choices"][0]["message"]["content"].lower()
            result = {
                "sentiment": "positive" if "positive" in output else "negative",
                "confidence": None,
            }
        else:
            return jsonify({"error": "Invalid model type."}), 400

        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(port=8080, debug=True)
