import requests

API_URL = "http://127.0.0.1:8000/analyze/"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}
data = {"text": "Hello, how are you?", "model": "llama"}

response = requests.post(API_URL, headers=headers, params=data)
print(response.json())  # Output: {"original_text": "Hello, how are you?", "translated_text": "Bonjour, comment ça va?"}
