import os
import json
from datetime import date
import time
from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

load_dotenv(override=True)

client = None
_configured = False

# Current Gemini model
GEMINI_MODEL = "gemini-3.6-flash"


def _configure_genai():
    """
    Initialize the Gemini client using the API key
    stored in the .env file.
    """

    global _configured, client

    # Already configured
    if _configured and client is not None:
        return True

    # Reload environment variables
    load_dotenv(override=True)

    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not key:
        print("ERROR: GEMINI_API_KEY / GOOGLE_API_KEY is missing.")
        _configured = False
        return False

    # Clean accidental quotes/spaces
    key = key.strip("'\" \n\r\t")

    try:
        client = genai.Client(api_key=key)

        _configured = True

        print("DEBUG: Gemini client initialized successfully.")
        print(f"DEBUG: Gemini model configured: {GEMINI_MODEL}")

        return True

    except Exception as e:
        print(f"ERROR: Failed to initialize Gemini client: {e}")

        client = None
        _configured = False

        return False


# ============================================================
# KNOWLEDGE BASE
# ============================================================

def load_laws():
    """
    Load the local legal knowledge base from laws.json.
    """

    try:
        file_path = os.path.join(
            os.path.dirname(__file__),
            "../data/laws.json"
        )

        with open(file_path, "r", encoding="utf-8") as f:
            laws = json.load(f)

        print(f"DEBUG: Loaded {len(laws)} laws from laws.json.")

        return laws

    except Exception as e:
        print(f"ERROR loading laws.json: {e}")
        return []


LAWS_DB = load_laws()


# ============================================================
# LAW SEARCH
# ============================================================

def search_laws(query: str):
    """
    Search the local laws database using keywords and titles.
    """

    if not query:
        return []

    query_lower = query.lower()

    results = []

    for law in LAWS_DB:

        keywords = law.get("keywords", [])

        # Make sure keywords are strings
        keyword_match = any(
            str(keyword).lower() in query_lower
            for keyword in keywords
        )

        title = law.get("title", "").lower()

        title_match = title and title in query_lower

        if keyword_match or title_match:
            results.append(law)

    return results


# ============================================================
# AI LEGAL RESPONSE
# ============================================================

def get_ai_response(question: str):
    """
    Generate an AI-powered legal awareness response.

    Workflow:

    User Question
        ↓
    Local laws.json search
        ↓
    Relevant legal context
        ↓
    Gemini prompt
        ↓
    Gemini response
    """

    if not question or not question.strip():
        return "Please enter a legal question."

    # --------------------------------------------------------
    # Search local legal database
    # --------------------------------------------------------

    relevant_laws = search_laws(question)

    context_text = ""

    if relevant_laws:

        context_text = (
            "\n\nRELEVANT LEGAL CONTEXT FROM LOCAL DATABASE:\n"
        )

        for law in relevant_laws:

            context_text += (
                f"- {law.get('title', 'Unknown')}: "
                f"{law.get('description', 'N/A')} "
                f"(Punishment: "
                f"{law.get('punishment', 'N/A')})\n"
            )

    else:

        context_text = (
            "\n\nNo directly matching law was found "
            "in the local database.\n"
        )

    # --------------------------------------------------------
    # Construct prompt
    # --------------------------------------------------------

    prompt = f"""
You are LawAid-X-Sanvidhan, an Indian legal awareness assistant.

Your purpose is to explain Indian laws and constitutional rights
in simple language for ordinary citizens.

{context_text}

IMPORTANT INSTRUCTIONS:

1. Use the provided legal context whenever it is relevant.
2. If the local context does not completely answer the question,
   use your general legal knowledge carefully.
3. Clearly indicate when the answer is general information.
4. Do not claim to be a lawyer.
5. Do not invent laws, sections, punishments, or legal procedures.
6. Explain difficult legal terminology in simple language.
7. Keep the answer concise but useful.
8. ALWAYS answer in English.

FORMATTING INSTRUCTIONS:

- Return HTML only.
- Use <h4> for headings.
- Use <p> for paragraphs.
- Use <ul> and <li> for lists.
- Use <strong> for important information.
- Do NOT use Markdown.
- Do NOT use ** or ##.
- Keep the HTML clean and safe.

USER QUESTION:

{question}
"""

    # --------------------------------------------------------
    # Configure Gemini
    # --------------------------------------------------------

    if not _configure_genai():

        return (
            "Configuration Error: Gemini API key is missing "
            "or could not be initialized. "
            "Please check your .env file."
        )

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    try:

        print(
            f"DEBUG: Sending request to Gemini model: "
            f"{GEMINI_MODEL}"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response or not response.text:
            return (
                "<h4>AI Service Error</h4>"
                "<p>The Gemini AI service returned an empty response.</p>"
                "<p>Please try again later.</p>"
            )

        print("DEBUG: Gemini response received successfully.")

        return response.text.strip()

    except Exception as e:

        error_msg = str(e)

        print(
            f"Gemini API Error in get_ai_response: "
            f"{error_msg}"
        )

        # Handle quota / rate-limit errors
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return (
                "<h4>AI Service Temporarily Unavailable</h4>"
                "<p>The Gemini API quota has been exceeded "
                "or the service is temporarily rate-limited.</p>"
                "<p>Please try again later or check the "
                "Gemini API quota and billing settings.</p>"
            )

        # Handle unavailable model
        if "404" in error_msg or "NOT_FOUND" in error_msg:
            return (
                "<h4>AI Model Unavailable</h4>"
                "<p>The configured Gemini model is currently "
                "not available for this API key.</p>"
                "<p>Please verify the Gemini API model availability.</p>"
            )

        # Handle temporary Gemini server problems
        if "503" in error_msg or "UNAVAILABLE" in error_msg:
            return (
                "<h4>Gemini Service Temporarily Unavailable</h4>"
                "<p>The Gemini AI service is currently experiencing "
                "high demand or a temporary server issue.</p>"
                "<p>Please try again in a few moments.</p>"
            )

        # Generic error
        return (
            "<h4>AI Service Error</h4>"
            "<p>LawAid-X-Sanvidhan could not connect to "
            "the Gemini AI service.</p>"
            "<p>Please try again later.</p>"
        )

# ============================================================
# TRANSLATION
# ============================================================

def translate_text(text: str, target_lang: str = "hi"):
    """
    Translate the AI response into the requested language.

    Currently the project primarily uses Hindi translation.
    """

    if not text:
        return ""

    if not _configure_genai():

        return (
            "Translation failed: Gemini API key is missing "
            "or could not be initialized."
        )

    prompt = f"""
Translate the following legal-awareness response into Hindi
using Devanagari script.

IMPORTANT:

1. Preserve all HTML tags exactly.
2. Do not translate HTML tags.
3. Translate only the visible text.
4. Keep legal terminology accurate.
5. Use simple Hindi that ordinary Indian citizens can understand.
6. Do not add explanations.
7. Return only the translated HTML.

HTML TEXT:

{text}
"""

    try:

        print(
            f"DEBUG: Translating using Gemini model: "
            f"{GEMINI_MODEL}"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response or not response.text:

            return "Translation failed: Empty response from AI."

        return response.text.strip()

    except Exception as e:

        error_msg = str(e)

        print(
            f"Gemini Translation Error: {error_msg}"
        )

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:

            return (
                "Translation temporarily unavailable "
                "because the Gemini API quota has been exceeded."
            )

        return (
            f"Translation failed: {error_msg}"
        )


# ============================================================
# LEGAL DOCUMENT GENERATOR
# ============================================================

def generate_legal_document(
    doc_type: str,
    full_name: str,
    address: str,
    subject: str,
    details: str
) -> str:

    """
    Generate a formal legal document using Gemini AI.
    """

    doc_type_labels = {

        "complaint-letter":
            "Formal Complaint Letter",

        "legal-notice":
            "Legal Notice",

        "rti-request":
            "RTI Application under Right to Information Act, 2005",
    }

    doc_label = doc_type_labels.get(
        doc_type.lower(),
        "Legal Document"
    )

    today = date.today().strftime("%d %B %Y")

    prompt = f"""
You are an expert Indian legal document drafting assistant.

Generate a professional {doc_label} using the information below.

IMPORTANT:

- Output ONLY plain text.
- Do NOT use Markdown.
- Do NOT use HTML.
- Do NOT use asterisks.
- Use proper document formatting.
- Include appropriate legal sections.
- Use formal but understandable language.
- Do not invent facts.
- Do not invent legal sections.
- Do not claim that the document guarantees a legal outcome.
- Include "Yours faithfully," followed by a signature line.

TODAY'S DATE:
{today}

SENDER DETAILS:

Name:
{full_name}

Address:
{address}

SUBJECT:

{subject}

FACTS / DETAILS:

{details}

Generate the complete document now.
"""

    # --------------------------------------------------------
    # Configure Gemini
    # --------------------------------------------------------

    if not _configure_genai():

        return _fallback_document(
            doc_label,
            full_name,
            address,
            subject,
            details,
            today
        )

    # --------------------------------------------------------
    # Generate document
    # --------------------------------------------------------

    try:

        print(
            f"DEBUG: Generating document using "
            f"Gemini model: {GEMINI_MODEL}"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return _fallback_document(
            doc_label,
            full_name,
            address,
            subject,
            details,
            today
        )

    except Exception as e:

        print(
            f"Gemini API Error in "
            f"generate_legal_document: {e}"
        )

        return _fallback_document(
            doc_label,
            full_name,
            address,
            subject,
            details,
            today
        )


# ============================================================
# FALLBACK DOCUMENT
# ============================================================

def _fallback_document(
    doc_label: str,
    full_name: str,
    address: str,
    subject: str,
    details: str,
    today: str
) -> str:

    """
    Basic document template used when Gemini is unavailable.
    """

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

I, therefore, request you to kindly look into this matter and take appropriate action at the earliest.

Thanking you,

Yours faithfully,

_________________________
{full_name}

Date: {today}

[This is a system-generated document template. Please review and modify it as needed before submission.]
"""