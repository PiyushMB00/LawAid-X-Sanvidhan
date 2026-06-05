# LawAid X Sanvidhan ⚖️🇮🇳

**LawAid X Sanvidhan** is an AI-powered legal awareness and assistance platform designed to make Indian law accessible to everyone. By combining a robust knowledge base of Indian laws (BNS, BNSS, etc.) with the power of Google Gemini AI, it provides instant legal guidance, document drafting, and emergency assistance.

---

## 🚀 Key Features

### 🤖 Legal AI Assistant
- **Chatbot integration** utilizing Gemini 2.0 / 1.5 for instant legal doubt resolution.
- **Multilingual Support**: Instant Hindi translation for all AI-generated advice.
- **Legal Context Awareness**: Automatically references a built-in database of Indian Penal Codes and punishments.

### 📜 Constitution Explainer
- Browse and search through various Articles and Rights.
- Simplified explanations of complex constitutional provisions.

### ✍️ Legal Document Generator
- Draft formal **Legal Notices**, **Complaint Letters**, and **RTI Applications** in seconds.
- Professional, court-ready templates powered by AI.

### 🛡️ SOS Shield & Emergency Directory
- One-tap emergency assistance.
- Access to vital contacts for legal aid and authorities.

### 📚 Rights Library
- Comprehensive educational guides on Child Rights, Women's Rights, Consumer Rights, and more.

---

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: HTML5, Vanilla CSS, JavaScript, Jinja2 Templates
- **AI Engine**: Google Gemini AI (via `google-generativeai`)
- **Database**: JSON-based local knowledge base
- **Environment**: Python Dotenv for secure configuration

---

## 📥 Installation & Setup

### 1. Prerequisite
Ensure you have **Python 3.10+** installed.

### 2. Clone the Repository
```bash
git clone <repository-url>
cd LawAid-X-Sanvidhan
```

### 3. Setup Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On MacOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables
Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```
> [!NOTE]
> Ensure you have the **"Generative Language API"** enabled in your [Google AI Studio](https://aistudio.google.com/app/apikey) or Google Cloud Console.

---

## 🏃 Running the Application

Start the development server:
```bash
python main.py
```
The application will be available at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📂 Project Structure

```text
 LawAid-X-Sanvidhan/
 ├── app/
 │   ├── static/          # CSS, Images, JS
 │   ├── templates/       # HTML Jinja2 Templates
 │   ├── services/        # AI logic, Translation, Document Logic
 │   ├── routes/          # API route definitions
 │   ├── data/            # Local JSON databases (laws.json)
 │   └── main.py          # FastAPI application entry
 ├── main.py              # Uvicorn runner
 ├── .env                 # API Key configuration
 ├── requirements.txt     # Python dependencies
 └── README.md            # You are here!
```

---

## ⚖️ Disclaimer
*LawAid X Sanvidhan provides informational guidance based on available legal data and AI. It is not a substitute for professional legal advice from a qualified advocate or lawyer.*
