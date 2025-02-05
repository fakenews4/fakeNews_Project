from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import os
import traceback
import asyncio
import ollama
from collections import Counter
from konlpy.tag import Okt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()

# 한국어 형태소 분석기 (Okt)
okt = Okt()

# Pydantic 모델들
class UrlRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

class SummarizeRequest(BaseModel):
    content: str

class TextRequest(BaseModel):
    content: str

class keywordRequest(BaseModel):
    content: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FastAPI 서버가 실행 중입니다!"}

@app.post("/keywords")
async def extract_keywords_from_content(request: UrlRequest):
    try:
        url = request.url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="웹 페이지 요청 실패")
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # 이미지, figcaption, title 속성이 있는 span 태그 제거
        for img in soup.find_all('img'):
            img.decompose()
        for figcaption in soup.find_all('figcaption'):
            figcaption.decompose()
        for span in soup.find_all('span', title=True):
            span.decompose()

        # 다양한 태그에서 본문 텍스트 추출
        article_content = ""
        for tag in ["article"]:
            for element in soup.find_all(tag):
                article_content += element.get_text(separator=" ") + " "

        if not article_content.strip():
            raise HTTPException(status_code=500, detail="크롤링된 콘텐츠가 없습니다.")

        # 키워드 추출 (상위 1개)
        keywords = extract_keywords(article_content, top_n=1)
        print("✅ 추출된 키워드:", keywords)

        return {"keywords": keywords}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"요청 중 오류 발생: {str(e)}")
    except Exception as e:
        print(f"🔥 서버 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        print(f"📩 사용자 질문: {request.question}")
        response = await asyncio.to_thread(
            ollama.chat,
            model='gemma2',
            messages=[
                {"role": "system", "content": "당신은 유용한 한국어 챗봇입니다."},
                {"role": "user", "content": request.question}
            ]
        )
        if "message" not in response:
            print(f"⚠️ Ollama 응답 오류: {response}")
            raise HTTPException(status_code=500, detail=f"Ollama 응답 오류: {response}")

        chatbot_reply = response["message"]
        print(f"🤖 챗봇 응답: {chatbot_reply}")
        return {"reply": chatbot_reply}

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"🔥 서버 오류 발생:\n{error_details}")
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")

@app.post("/crawl")
async def crawl_url(request: UrlRequest):
    url = request.url
    try:
        options = Options()
        options.headless = True
        options.add_argument("--ignore-certificate-errors")
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)

        try:
            content = driver.find_element(By.TAG_NAME, 'article').text
        except Exception as e:
            content = ""
            print(f"콘텐츠 추출 실패: {e}")

        driver.quit()

        if content:
            return {"extracted_content": content}
        else:
            raise HTTPException(status_code=500, detail="웹 페이지에서 콘텐츠를 추출할 수 없습니다.")

    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"크롤링 중 오류 발생: {str(e)}")

@app.post("/summarize")
async def summarize_content(request: SummarizeRequest):
    try:
        print(f"📩 요약 요청된 콘텐츠: {request.content}")
        summarize_question = f"다음 내용을 요약해 주세요: {request.content}"
        response = await asyncio.to_thread(
            ollama.chat,
            model='gemma2',
            messages=[
                {"role": "system", "content": "당신은 유용한 한국어 챗봇입니다."},
                {"role": "user", "content": summarize_question}
            ]
        )
        if "message" not in response:
            raise HTTPException(status_code=500, detail="Ollama 응답 오류")
        summary = response["message"]
        print(f"🤖 요약된 내용: {summary}")
        return {"summary": summary}
    except Exception as e:
        print(f"🔥 서버 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")

class TextRequest(BaseModel):
    content: str

def extract_keywords(text, top_n=1):
    """텍스트에서 핵심 키워드 추출"""
    words = okt.pos(text)
    print("📌 형태소 분석 결과:", words)  # 🔥 디버깅 로그 추가

    # 고유명사(Nnp)와 일반명사(Noun) 추출
    proper_nouns = [word for word, pos in words if pos == 'Nnp']
    common_nouns = [word for word, pos in words if pos == 'Noun']
    print("✅ 고유명사:", proper_nouns)  # 🔥 로그 추가
    print("✅ 일반명사:", common_nouns)

    # 고유명사와 일반명사 합치기
    all_nouns = proper_nouns + common_nouns
    all_nouns = [word for word in all_nouns if len(word) > 1]  # 길이가 1보다 큰 단어만 필터링

    # 명사 카운팅
    word_counts = Counter(all_nouns)
    filtered_words = [word for word, _ in word_counts.most_common(top_n) if len(word) > 1]
    
    # 디버깅 출력
    print("✅ 추출된 키워드:", filtered_words)
    
    return filtered_words if filtered_words else ["키워드 없음"]


@app.post("/upload")
async def upload_file(news_file: UploadFile = File(...)):  # ✅ news_file의 이름이 맞는지 확인!
    if not news_file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="지원되지 않는 파일 형식입니다. .txt 파일만 업로드하세요.")

    content = await news_file.read()  # 🔥 파일 읽기
    text_content = content.decode("utf-8").strip()

    print("📂 [UPLOAD] 파일 내용 (200자까지):", text_content[:200])  # 🔥 첫 200자만 출력

    if not text_content:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")

    return {"success": True, "content": text_content}

async def prevent_get_upload():
    raise HTTPException(status_code=405, detail="이 경로는 POST 요청만 지원합니다.")

@app.post("/keywords_from_text")
async def extract_keywords_from_text(data: dict):
    content = data.get("content", "").strip()
    
    print("🔍 키워드 추출 요청된 텍스트:", content[:200])  # 🔥 첫 200글자 출력

    if not content:
        raise HTTPException(status_code=400, detail="추출할 텍스트가 없습니다.")

    keywords = extract_keywords(content, top_n=1)  # ✅ 키워드 1개 추출
    print("✅ 추출된 키워드:", keywords)

    return {"success": True, "keywords": keywords}

