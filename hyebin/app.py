from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

from static.handler.crawl import crawl_url
from static.handler.summarize import summarize_content
from static.handler.keywords import extract_keywords_from_content, extract_keywords_from_text
from static.handler.chatbot import ask_question
from static.handler.file_handler import upload_file

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델 정의
class UrlRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

class SummarizeRequest(BaseModel):
    content: str

@app.get("/")
async def root():
    return {"message": "FastAPI 서버가 실행 중입니다!"}

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
