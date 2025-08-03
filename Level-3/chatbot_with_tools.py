import os
import json
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
from calculator_tool import calculate
from translator_tool import translate_to_german

# Load API key from .env
load_dotenv("key.env")
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in key.env")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-8b-8192"
LOG_FILE = "interaction_log.json"
MEMORY_LIMIT = 10  # Number of exchanges to keep in memory


# ------------------- Utility Functions -------------------

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

def extract_full_math_expressions(text):
    symbolic = re.findall(r'(?:\d+(?:\.\d+)?\s*[\+\-\*/%]\s*)+\d+(?:\.\d+)?', text)
    natural = re.findall(r'(add|subtract|multiply|divide)\s+(\d+)\s+(and|by)?\s*(\d+)', text, re.IGNORECASE)
    converted = []
    for op, a, _, b in natural:
        op = op.lower()
        if op == "add": converted.append(f"{a} + {b}")
        elif op == "subtract": converted.append(f"{a} - {b}")
        elif op == "multiply": converted.append(f"{a} * {b}")
        elif op == "divide": converted.append(f"{a} / {b}")
    return symbolic + converted

def detect_translation(text):
    return "translate" in text.lower() and "to german" in text.lower()

def extract_translation_texts(text):
    return re.findall(r'translate\s+"?([^"\n]+?)"?\s+to german', text, re.IGNORECASE)

def ask_llm(question, memory_messages):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    base_messages = [{"role": "system", "content": "You are a helpful assistant."}]
    data = {
        "model": MODEL_NAME,
        "messages": base_messages + memory_messages + [{"role": "user", "content": question}]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


# ------------------- Main Chatbot -------------------

def main():
    logs = load_logs()
    memory = []  # In-memory chat history

    print("\U0001F916 Multitasking Chatbot (LLM + Translator + Calculator). Type 'exit' to quit.")

    while True:
        user_input = input("\nAsk a question: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        responses = []

        # --- Translation ---
        if detect_translation(user_input):
            for text in extract_translation_texts(user_input):
                try:
                    translated = translate_to_german(text)
                    responses.append(f"🇩🇪 Translated: {text} → {translated}")
                except Exception as e:
                    responses.append(f"❌ Translation error for '{text}': {e}")

        # --- Math ---
        for expr in extract_full_math_expressions(user_input):
            try:
                result = calculate(expr)
                responses.append(f"🧮 Math result: {expr} = {result}")
            except Exception as e:
                responses.append(f"❌ Math error in '{expr}': {e}")

        # --- General LLM Response ---
        try:
            llm_response = ask_llm(user_input, memory)
            responses.insert(0, f"🧠 General Answer: {llm_response}")
        except Exception as e:
            responses.append(f"❌ LLM error: {e}")

        # Display responses
        print("\n🧠 Response:")
        for r in responses:
            print(r)

        # --- Update memory ---
        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": "\n".join(responses)})
        if len(memory) > MEMORY_LIMIT * 2:
            memory = memory[-MEMORY_LIMIT*2:]

        # --- Save to log file ---
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "question": user_input,
            "answer": responses
        })
        save_logs(logs)

if __name__ == "__main__":
    main()