import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Find the root directory (.env location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(BASE_DIR, ".env")

# Load environment variable with absolute path and override=True
load_dotenv(dotenv_path=env_path, override=True)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Load Knowledge Base
def load_laws():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "../data/laws.json")
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading laws.json: {e}")
        return []

LAWS_DB = load_laws()

def search_laws(query: str):
    query = query.lower()
    results = []
    for law in LAWS_DB:
        # Simple keyword match in database
        if any(k in query for k in law.get("keywords", [])) or \
           law.get("title", "").lower() in query:
            results.append(law)
    return results

def get_ai_response(question: str):
    relevant_laws = search_laws(question)
    
    context_text = ""
    if relevant_laws:
        context_text = "\n\nRelevant Legal Context found in database:\n"
        for law in relevant_laws:
            context_text += f"- {law.get('title', 'Unknown')}: {law.get('description', 'N/A')} (Punishment: {law.get('punishment', 'N/A')})\n"
    
    prompt = f"""
    You are a legal awareness assistant for India.
    
    {context_text}
    
    Use the above legal context if relevant. If the context doesn't answer the question completely, use your general knowledge but mention that.
    Explain the answer in very simple language.
    ALWAYS answer in English.
    
    FORMATTING INSTRUCTIONS:
    - Use HTML tags for formatting.
    - Use <h4> for headings.
    - Use <ul> and <li> for lists.
    - Use <strong> for emphasis.
    - Do NOT use markdown (like ** or ##).
    - Keep it clean and structured.
    
    Question: {question}
    """

    try:
        if not api_key:
            return "Configuration Error: GEMINI_API_KEY is missing. Please check your .env file."
            
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return "I apologize, but I encountered an error connecting to the AI service. Please try again later."

def translate_text(text: str, target_lang: str = 'hi'):
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        prompt = f"""Translate the following text to Hindi (Devanagari script). 
        
        INSTRUCTIONS:
        - Keep all legal terms accurate but simple.
        - PRESERVE all original HTML tags intact (like <h4>, <ul>, <li>, <strong>). 
        - Do not translate the tags themselves, only the content inside them.
        
        Text: {text}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Translation failed: {str(e)}"
