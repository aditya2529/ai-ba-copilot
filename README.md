# 🚀 AI Requirement Intelligence Copilot (MVP)

## 🧠 Overview
This project is a lightweight AI-powered system designed to transform raw meeting notes into **high-quality, structured requirements**.

Unlike basic AI generators, this system focuses on:
- Requirement clarity
- Validation
- Risk identification
- Test readiness

---

## 🎯 Problem Statement
In real-world projects, requirement quality is a major bottleneck:

- Ambiguous user stories  
- Missing edge cases  
- Undetected dependencies  
- Rework during development  

This leads to delays, misalignment, and inefficiencies.

---

## 💡 Solution
This project introduces a **Requirement Intelligence Layer** that:

✔ Converts meeting notes → structured user stories  
✔ Identifies gaps and ambiguities  
✔ Detects risks and dependencies  
✔ Generates test cases  
✔ Provides estimation with reasoning  

---

## ⚙️ Features

- 🧾 User Story Generation  
- ✅ Validation Engine (ambiguity & completeness check)  
- ⚠️ Risk & Dependency Detection  
- 🧪 Test Case Generation  
- 📊 Estimation with reasoning  

---

## 🏗️ Architecture (MVP)


Meeting Notes
↓
LLM (Local - Ollama / Phi3)
↓
Structured Output
↓
(User Story + Validation + Risks + Tests + Estimation)



---

## 🛠️ Tech Stack

- Python  
- Ollama (Local LLM)  
- Phi3 Model (lightweight, runs on 8GB RAM)  

---

## 🚀 How to Run

### 1. Install Ollama
https://ollama.com/download

### 2. Pull model


ollama run phi3


### 3. Install Python dependencies

pip install ollama python-dotenv


### 4. Run the application

python ai_ba_copilot.py


---

## 🧪 Sample Input


User should login using email and OTP.
OTP expires in 5 minutes.
System should handle invalid OTP.
Integration with SMS service required.


---

## 🔍 Sample Output

- User Story  
- Validation Issues  
- Risks & Dependencies  
- Test Cases  
- Estimation  

---

## 🧠 Key Differentiation

This is not just a generator.

It acts as a **thinking layer** between:

Raw Input → Execution (Devs / AI Agents like Devin)


It ensures:
👉 Better requirement quality before execution  

---

## 🚀 Future Enhancements

- Streamlit UI (web interface)  
- RAG (context-aware generation using BRDs / past stories)  
- Jira / Confluence integration  
- Multi-agent workflow  

---

## 👨‍💻 Author

Aditya  
AI + Product Enthusiast | Building AI-powered BA tools  

---

## ⭐ Why this project matters

> Improving requirement quality = improving delivery outcomes

This project aims to bridge the gap between:
- Business understanding  
- Technical execution  

---
