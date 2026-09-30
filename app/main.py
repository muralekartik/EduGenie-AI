from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.schemas import ExplainRequest, QnARequest, QuizRequest, SummarizeRequest
from app.services.ai_service import AIService

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.app_name,
    description="Google Gemini Powered Learning Assistant",
    version=settings.app_version,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")
ai_service = AIService()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": settings.app_name,
    }


@app.post("/api/qna")
async def qna(request: QnARequest):
    return await ai_service.answer_question(
        question=request.question,
        context=request.context,
    )


@app.post("/api/explain")
async def explain(request: ExplainRequest):
    return await ai_service.explain_topic(
        topic=request.topic,
        level=request.level,
    )


@app.post("/api/summarize")
async def summarize(request: SummarizeRequest):
    return await ai_service.summarize_text(
        text=request.text,
        length=request.length,
    )


@app.post("/api/quiz")
async def quiz(request: QuizRequest):
    return await ai_service.generate_quiz(
        topic=request.topic,
        difficulty=request.difficulty,
    )


@app.get("/api/learn/recommendations")
async def recommendations(topic: str = ""):
    return await ai_service.get_recommendations(topic)
