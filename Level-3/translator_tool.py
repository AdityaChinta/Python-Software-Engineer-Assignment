import requests
import os
from dotenv import load_dotenv

load_dotenv("key.env")
api_key = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-8b-8192"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def translate_to_german(text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f'Translate the following English text to German:\n\n"{text}"'
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
