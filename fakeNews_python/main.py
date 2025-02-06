from fastapi import FastAPI, HTTPException, File, UploadFile
from routers import news, fake_news  # ✅ 라우터 추가
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
from fastapi.staticfiles import StaticFiles
import os
from handler.crawl import crawl_url
from handler.summarize import summarize_content
from handler.keywords import extract_keywords_from_content, extract_keywords_from_text
from handler.chatbot import ask_question
from handler.file_handler import upload_file


print("✅ FastAPI 서버 시작 중...")  # ✅ 서버 시작 확인 로그


app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (보안상 필요하다면 특정 도메인만 허용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # main.py가 있는 폴더 기준
STATIC_DIR = os.path.join(BASE_DIR, "static")

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(news.router)
# app.include_router(fake_news.router)

@app.get("/")
async def read_root():
    file_path = os.path.join(os.getcwd(), "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)

print("✅ FastAPI 서버가 정상적으로 실행되었습니다!")  # ✅ 실행 완료 확인 로그


# Pydantic 모델 정의
class UrlRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

class SummarizeRequest(BaseModel):
    content: str

@app.get("/")
async def read_root():
    file_path = os.path.join(os.getcwd(), "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)

# 📌 크롤링 엔드포인트
@app.post("/crawl")
async def crawl(request: UrlRequest):
    return await crawl_url(request.url)

# 📌 요약 엔드포인트
@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    return await summarize_content(request.content)

# 📌 키워드 추출 (URL)
@app.post("/keywords")
async def extract_keywords(request: UrlRequest):
    return await extract_keywords_from_content(request.url)

# 📌 키워드 추출 (텍스트)
@app.post("/keywords_from_text")
async def extract_keywords_text(data: dict):
    return await extract_keywords_from_text(data)

# 📌 챗봇 엔드포인트
@app.post("/ask")
async def ask_chatbot(request: QuestionRequest):
    return await ask_question(request.question)

# 📌 파일 업로드 엔드포인트
@app.post("/upload")
async def upload(news_file: UploadFile = File(...)):
    return await upload_file(news_file)

