from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.services.ai_service import get_ai_response, translate_text, generate_legal_document
from app.routes import sos
import uvicorn
import os
import json
from dotenv import load_dotenv

# Initialize environment variables at entry point
load_dotenv(override=True)
if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY not found in environment variables!")

# Helper for cache busting and safe routing
def get_url_for(name, **kwargs):
    if name == "static":
        filename = kwargs.get("filename", "")
        return f"/static/{filename}?v=1.5"
    # Fallback for non-static routes if needed, though usually FastAPI's own url_for should be used
    return "#"

app = FastAPI(title="Lawaid X Sanvidhan Backend")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Safer template global for site-wide static versioning
templates.env.globals["url_for"] = get_url_for

@app.get("/api/version")
async def get_version():
    return {"version": "v2-consolidated", "status": "active"}

# Robust API routes to avoid ghosting/routing conflicts
@app.post("/api/ask")
async def ask_legal_ai(request: Request):
    try:
        data = await request.json()
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
            
        # Accept both message and question fields for compatibility
        message = data.get("message") or data.get("question")
        if not message:
            return {"error": "No message provided"}, 400
        answer = get_ai_response(message)
        return {"response": answer}
    except Exception as e:
        print(f"Server Error in /api/ask: {e}")
        return {"error": "Internal Server Error", "detail": str(e)}, 500

@app.post("/api/translate")
async def translate_legal_text(request: Request):
    try:
        data = await request.json()
        text = data.get("text")
        if not text:
            return {"error": "No text provided"}, 400
        translated = translate_text(text)
        return {"translation": translated}
    except Exception as e:
        print(f"Server Error in /api/translate: {e}")
        return {"error": "Internal Server Error", "detail": str(e)}, 500

@app.post("/api/generate-document")
async def generate_document(request: Request):
    try:
        data = await request.json()
        doc_type = data.get("doc_type", "complaint-letter")
        full_name = data.get("full_name", "")
        address = data.get("address", "")
        subject = data.get("subject", "")
        details = data.get("details", "")

        if not all([full_name, address, subject, details]):
            return JSONResponse({"error": "All fields are required."}, status_code=400)

        document_text = generate_legal_document(
            doc_type=doc_type,
            full_name=full_name,
            address=address,
            subject=subject,
            details=details
        )
        return JSONResponse({"document": document_text})
    except Exception as e:
        print(f"Server Error in /api/generate-document: {e}")
        return JSONResponse({"error": "Internal Server Error", "detail": str(e)}, status_code=500)

app.include_router(sos.router, prefix="/sos", tags=["SOS"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/constitution", response_class=HTMLResponse)
async def constitution(request: Request):
    return templates.TemplateResponse("constitution.html", {"request": request})

@app.get("/document-generator", response_class=HTMLResponse)
async def document_generator(request: Request):
    return templates.TemplateResponse("document-generator.html", {"request": request})

@app.get("/generator/{doc_type}", response_class=HTMLResponse)
async def generator_detail(request: Request, doc_type: str):
    doc_type = doc_type.lower()
    return templates.TemplateResponse("generator-detail.html", {"request": request, "doc_type": doc_type})

@app.get("/rights-library", response_class=HTMLResponse)
async def rights_library(request: Request):
    return templates.TemplateResponse("rights-library.html", {"request": request})

@app.get("/rights-library/{category}", response_class=HTMLResponse)
async def rights_detail(request: Request, category: str):
    # Ensure category is lowercase for template matching or logic
    category = category.lower()
    return templates.TemplateResponse("rights-detail.html", {"request": request, "category": category})

@app.get("/rightnow", response_class=HTMLResponse)
async def rightnow(request: Request):
    return templates.TemplateResponse("rightnow.html", {"request": request})

@app.get("/rightnow/{topic}", response_class=HTMLResponse)
async def rightnow_detail(request: Request, topic: str):
    topic = topic.lower()
    return templates.TemplateResponse("rightnow-detail.html", {"request": request, "topic": topic})

@app.get("/emergency-directory", response_class=HTMLResponse)
async def emergency_directory(request: Request):
    return templates.TemplateResponse("emergency-directory.html", {"request": request})

@app.get("/legal-aid", response_class=HTMLResponse)
async def legal_aid(request: Request):
    return templates.TemplateResponse("legal-aid.html", {"request": request})

@app.get("/sos-shield", response_class=HTMLResponse)
async def sos_shield(request: Request):
    return templates.TemplateResponse("sos-shield.html", {"request": request})

@app.get("/articles", response_class=HTMLResponse)
async def articles(request: Request):
    return templates.TemplateResponse("articles.html", {"request": request})

@app.get("/documents", response_class=HTMLResponse)
async def documents(request: Request):
    return templates.TemplateResponse("documents.html", {"request": request})


@app.get("/api/laws")
async def get_all_laws():
    try:
        file_path = os.path.join("app", "data", "laws.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error serving laws.json: {e}")
        return {"error": "Internal Server Error", "detail": str(e)}, 500


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
