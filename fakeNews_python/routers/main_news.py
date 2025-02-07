from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from handler.crawl import crawl_url
from handler.summarize import summarize_content
from handler.keywords import extract_keywords_from_content, extract_keywords_from_text
from handler.chatbot import ask_question
from handler.file_handler import upload_file

router = APIRouter()

# ✅ Pydantic 모델 정의
class UrlRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

class SummarizeRequest(BaseModel):
    content: str

# ✅ 크롤링 엔드포인트
@router.post("/crawl")
async def crawl(request: UrlRequest):
    return await crawl_url(request.url)

# ✅ 요약 엔드포인트
@router.post("/summarize")
async def summarize(request: SummarizeRequest):
    return await summarize_content(request.content)

# ✅ 키워드 추출 (URL)
@router.post("/keywords")
async def extract_keywords(request: UrlRequest):
    return await extract_keywords_from_content(request.url)

# ✅ 키워드 추출 (텍스트)
@router.post("/keywords_from_text")
async def extract_keywords_text(data: dict):
    return await extract_keywords_from_text(data)

# ✅ 챗봇 엔드포인트
@router.post("/ask")
async def ask_chatbot(request: QuestionRequest):
    return await ask_question(request.question)

# ✅ 파일 업로드 엔드포인트
@router.post("/upload")
async def upload(news_file: UploadFile = File(...)):
    return await upload_file(news_file)
