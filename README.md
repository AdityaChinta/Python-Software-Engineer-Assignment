# Multitasking CLI Chatbot (LLM + Translator + Calculator)

A powerful, multitasking Python chatbot that:

- Acts as a general-purpose AI assistant
- Solves math expressions in natural or symbolic language
- Translates English phrases to German
- Maintains conversation memory and logs interactions

Built using the Groq API with Meta's `llama3-8b-8192` model.

---

## Features

- Accepts multi-step input like:  
  `"Translate 'good morning' to German and multiply 12 by 5"`
- General chatbot intelligence via LLaMA-3
- Math parser and calculator with symbolic and natural language support
- English-to-German translation tool
- Persistent memory for smoother LLM responses
- JSON log of every interaction in `interaction_log.json`

---

## 🗂Project Structure

---

## Setup Instructions

1. **Clone the repo**

bash
git clone https://github.com/AdityaChinta/Python-Software-Engineer-Assignment.git
cd multitask-chatbot

2. **Install Requirements**

pip install -r requirements.txt

3. **Set-up your Groq API-key**

GROQ_API_KEY=your_groq_api_key_here

4.**Run your bot**

Choose the level of the LLM Chatbot and run the python files

5.**Memory and Logs**

The interactions with the chatbot are recorded in memory to provide context to the LLM and interaction_log.json stores the interactions with the timestamp

##Dependencies

Python 3.8+

##Notes

You are usng Groq API with the llama3-8b-8192 LLM

##Credits
Groq:for hosting LLM
Meta:for LLaMa 3
