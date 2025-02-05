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

def extract_keywords(text, top_n=10):
    """본문에서 고유명사와 명사를 우선순위로 추출하는 함수"""
    # 먼저, 전체 명사를 추출
    words = okt.pos(text)  # (단어, 품사) 튜플 리스트

    # 고유명사와 일반 명사 추출
    proper_nouns = [word for word, pos in words if pos == 'Nnp']
    common_nouns = [word for word, pos in words if pos == 'Noun']

    # 고유명사가 있으면 일반 명사는 제외, 없으면 모두 포함
    if proper_nouns:
        all_nouns = proper_nouns
    else:
        all_nouns = proper_nouns + common_nouns

    # 두 글자 이상의 단어만 필터링
    all_nouns = [word for word in all_nouns if len(word) > 1]

    word_counts = Counter(all_nouns)
    keywords = [word for word, _ in word_counts.most_common(top_n)]
    if not keywords:
        print("⚠️ 키워드가 추출되지 않았습니다.")
    return keywords

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
        response = requests.get(url)
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

        # article 태그만 선택하여 텍스트 추출
        article_content = ""
        article_tags = soup.find_all('article')
        for article in article_tags:
            article_content += article.get_text(separator=" ")

        if not article_content:
            raise HTTPException(status_code=500, detail="크롤링된 콘텐츠가 없습니다.")

        # 키워드 추출 (상위 1개)
        keywords = extract_keywords(article_content, top_n=1)
        print("✅ 추출된 키워드:", keywords)
        
        # 만약 화면에 표시하지 않으려면, "message" 필드만 반환할 수도 있습니다.
        return {"keywords": keywords}

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

@app.post("/upload")
async def upload_file(news_file: UploadFile = File(...)):
    try:
        file_location = f"temp_files/{news_file.filename}"
        os.makedirs("temp_files", exist_ok=True)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(news_file.file, f)
        
        if news_file.filename.endswith('.txt'):
            with open(file_location, "r", encoding="utf-8") as file:
                file_content = file.read()
            return {"success": True, "message": "파일이 성공적으로 업로드되었습니다!", "content": file_content}
        else:
            return {"success": False, "message": "업로드된 파일은 txt 파일이어야 합니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류 발생: {str(e)}")

