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


def generate_legal_document(doc_type: str, full_name: str, address: str, subject: str, details: str) -> str:
    """Generate a formal legal document using Gemini AI and return plain text."""

    doc_type_labels = {
        "complaint-letter": "Formal Complaint Letter",
        "legal-notice": "Legal Notice",
        "rti-request": "RTI Application under Right to Information Act, 2005",
    }
    doc_label = doc_type_labels.get(doc_type.lower(), "Legal Document")

    today = __import__('datetime').date.today().strftime("%d %B %Y")

    prompt = f"""You are an expert Indian legal document drafter. 
Generate a complete, professional, and court-ready {doc_label} based on the information below.

STRICT FORMATTING RULES:
- Output ONLY plain text. No markdown, no HTML, no asterisks, no bullet symbols.
- Use proper letter/document formatting with line breaks.
- Include all standard legal sections for the document type.
- Use formal, legally sound language appropriate for Indian courts/authorities.
- At the end include: "Yours faithfully," followed by a blank signature line and the sender's name.
- TODAY'S DATE: {today}

SENDER DETAILS:
Name: {full_name}
Address: {address}

SUBJECT / PURPOSE: {subject}

FACTS / DETAILS:
{details}

Generate the complete {doc_label} now:"""

    try:
        if not api_key:
            return _fallback_document(doc_label, full_name, address, subject, details, today)

        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error in generate_legal_document: {str(e)}")
        return _fallback_document(doc_label, full_name, address, subject, details, today)


def _fallback_document(doc_label: str, full_name: str, address: str, subject: str, details: str, today: str) -> str:
    """Returns a basic template document if AI is unavailable."""
    return f"""Date: {today}

From:
{full_name}
{address}

To,
The Concerned Authority,
[Name of Authority / Department]
[Address of Authority]

Subject: {subject}

Respected Sir/Madam,

I, {full_name}, residing at the address mentioned above, hereby bring to your kind notice the following matter:

{details}

I, therefore, request you to kindly look into this matter and take appropriate action at the earliest. I hope this matter will receive your urgent attention.

Thanking you,

Yours faithfully,

_________________________
{full_name}
Date: {today}

[This is a system-generated document template. Please review and modify as needed before submission.]"""

