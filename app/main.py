from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.services.ai_service import get_ai_response, translate_text
from app.routes import sos
import uvicorn

app = FastAPI(title="Lawaid X Sanvidhan Backend")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates.env.globals["url_for"] = lambda name, **kwargs: f"/{name}/{kwargs.get('filename', '')}" if name == "static" else "#"

@app.get("/api/version")
async def get_version():
    return {"version": "v2-consolidated", "status": "active"}

# Robust API routes to avoid ghosting/routing conflicts
@app.post("/api/ask")
async def ask_legal_ai(request: Request):
    try:
        data = await request.json()
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

@app.get("/rights-library", response_class=HTMLResponse)
async def rights_library(request: Request):
    return templates.TemplateResponse("rights-library.html", {"request": request})

@app.get("/rightnow", response_class=HTMLResponse)
async def rightnow(request: Request):
    return templates.TemplateResponse("rightnow.html", {"request": request})

@app.get("/sos-shield", response_class=HTMLResponse)
async def sos_shield(request: Request):
    return templates.TemplateResponse("sos-shield.html", {"request": request})

@app.get("/articles", response_class=HTMLResponse)
async def articles(request: Request):
    return templates.TemplateResponse("articles.html", {"request": request})

@app.get("/documents", response_class=HTMLResponse)
async def documents(request: Request):
    return templates.TemplateResponse("documents.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
