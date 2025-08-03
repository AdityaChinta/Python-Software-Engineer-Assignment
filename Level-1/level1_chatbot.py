import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load Groq API key from key.env
load_dotenv("key.env")
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY not found in key.env.")
    exit()

# API setup
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"
HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Log file path
LOG_FILE = "interaction_log.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

def ask_llm(prompt):
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who answers step-by-step."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=data)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()

def main():
    logs = load_logs()
    print("🤖 Groq LLaMA3 Chatbot. Type 'exit' to quit.")

    while True:
        user_input = input("\nAsk a question: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = ask_llm(user_input)
            print("\n" + response)
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "question": user_input,
                "answer": response
            })
            save_logs(logs)
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
