import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Global config flag
_configured = False

def _configure_genai():
    global _configured
    if not _configured:
        load_dotenv(override=True)
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if key:
            # Deep clean the key
            key = key.strip("'\" \n\r\t")
            # Force transport='rest' and try to specify API version v1
            try:
                genai.configure(api_key=key, transport='rest', client_options={"api_version": "v1"})
                _configured = True
                print("DEBUG: Gemini configured with v1 REST transport.")
            except Exception as e:
                print(f"DEBUG: Failed to configure with v1, trying default: {e}")
                genai.configure(api_key=key)
                _configured = True
        return key
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Load Knowledge Base
def load_laws():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "../data/laws.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading laws.json: {e}")
        return []

LAWS_DB = load_laws()

def search_laws(query: str):
    if not query:
        return []
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
        key = _configure_genai()
        if not key:
            return "Configuration Error: GEMINI_API_KEY is missing. Please check your .env file."
            
        # Robust fallback strategy using EXACT confirmed models for this key
        models_to_try = [
            'gemini-2.0-flash', 
            'gemini-flash-latest',
            'gemini-pro-latest',
            'gemini-2.0-flash-lite-preview-02-05',
            'gemini-1.5-flash', # Keeping as fallback
            'gemini-pro'
        ]
        
        last_exception = None

        # Diagnostic: Try to list models once to see what's available
        if _configured:
            try:
                available_models = [m.name for m in genai.list_models()]
                print(f"DEBUG: Available models for this key: {available_models}")
            except Exception as e:
                print(f"DEBUG: Could not list models: {e}")

        for model_name in models_to_try:
            try:
                print(f"DEBUG: Trying model {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                print(f"DEBUG: Model {model_name} failed: {e}")
                
                # If it's a key error, stop trying models
                if "api_key_invalid" in error_str or "unauthorized" in error_str:
                    break
                    
                continue
        
        # If all newer models fail, it's likely a project permissions issue
        if last_exception:
            raise last_exception
        return "I apologize, but I could not find a working AI model for your project. Please ensure 'Generative Language API' is enabled in your Google Cloud console."

    except Exception as e:
        error_msg = str(e)
        print(f"Gemini API Error: {error_msg}")
        return f"I apologize, but I encountered an error connecting to the AI service: {error_msg}. Please ensure your API key is valid and the Generative Language API is enabled for your project."

def translate_text(text: str, target_lang: str = 'hi'):
    try:
        _configure_genai()
        prompt = f"""Translate the following text to Hindi (Devanagari script). 
        
        INSTRUCTIONS:
        - Keep all legal terms accurate but simple.
        - PRESERVE all original HTML tags intact (like <h4>, <ul>, <li>, <strong>). 
        - Do not translate the tags themselves, only the content inside them.
        
        Text: {text}"""

        # Fallback for translation using confirmed models
        for model_name in ['gemini-2.0-flash', 'gemini-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
            except:
                continue
        return "Translation failed: No available models found or key is invalid for translation."
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
        key = _configure_genai()
        if not key:
            return _fallback_document(doc_label, full_name, address, subject, details, today)

        for model_name in ['gemini-2.0-flash', 'gemini-flash-latest', 'gemini-1.5-flash', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text.strip()
            except:
                continue
        
        return _fallback_document(doc_label, full_name, address, subject, details, today)
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