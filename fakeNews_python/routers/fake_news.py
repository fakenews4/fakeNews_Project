import os
<<<<<<< HEAD
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
=======
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import LlamaForCausalLM, LlamaTokenizer
>>>>>>> 2622a424821b655ee8e8a9ba0e488f99d2f6155f

# ✅ FastAPI 라우터 설정
router = APIRouter()

<<<<<<< HEAD
# ✅ KcELECTRA 모델 경로 설정
MODEL_PATH = os.path.join("D:/fakeNews_Project/fakeNews_python/models/kcelectra-news-finetuned")

# ✅ 라벨 매핑 (0: FAKE, 1: REAL)
LABELS = {"LABEL_0": "FAKE", "LABEL_1": "REAL"}  # KcELECTRA의 라벨과 동일한지 확인 필요

# ✅ KcELECTRA 모델 로드
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model, framework="pt")
=======
# ✅ 구글 팩트체크 API 키 설정
FACT_CHECK_API_KEY = os.getenv("FACT_CHECK")

# ✅ KoAlpaca 모델 로컬 경로 (config.json이 있는 폴더)
MODEL_DIR = "D:/fakeNews_Project/fakeNews_python/models/koalpaca_model/models--beomi--KoAlpaca/snapshots/model"  # 본인의 모델 경로로 변경

# ✅ KoAlpaca 모델 로드
try:
    tokenizer = LlamaTokenizer.from_pretrained(MODEL_DIR, legacy=False)
    model = LlamaForCausalLM.from_pretrained(MODEL_DIR)
>>>>>>> 2622a424821b655ee8e8a9ba0e488f99d2f6155f
except Exception as e:
    raise RuntimeError(f"KoAlpaca 모델 로딩 실패: {str(e)}")

<<<<<<< HEAD
# ✅ 요청 데이터 형식
=======
# ✅ 요청 데이터 형식 정의
>>>>>>> 2622a424821b655ee8e8a9ba0e488f99d2f6155f
class NewsRequest(BaseModel):
    content: str  # 뉴스 기사 or 검증할 주장

<<<<<<< HEAD
# ✅ 가짜뉴스 판별 API (순수 모델만 사용)
@router.post("/predict")
def predict_news(news_request: NewsRequest):
    """가짜 뉴스 판별 API (전처리 없이 모델만 사용)"""
    try:
        # ✅ KcELECTRA 모델 예측 (가짜뉴스 판별)
        result = classifier(news_request.content)[0]  
        label_str = result["label"]  
        label_name = LABELS.get(label_str, "UNKNOWN")

        return {
            "message": "Prediction successful",
            "label": label_name,  # ✅ "FAKE" 또는 "REAL"
            "score": result["score"]  # ✅ 신뢰도 점수
=======
# ✅ 1️⃣ 구글 팩트체크 API 호출 함수
def fact_check_google(query):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={FACT_CHECK_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None  # API 호출 실패 시 None 반환

    data = response.json()
    
    if "claims" in data and len(data["claims"]) > 0:
        return data["claims"]  # 검증된 기록이 있으면 반환
    return None  # 검증된 기록이 없으면 None 반환

# ✅ 2️⃣ KoAlpaca 모델 기반 분석 함수 (로컬 실행)
def analyze_with_koalpaca(question):
    """로컬 KoAlpaca 모델을 사용하여 뉴스 검증"""
    try:
        prompt = f"{question} 이 주장에 대한 신뢰도를 평가해줘."

        # ✅ 모델 입력 토큰화
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        # ✅ 모델 실행 (문장 생성)
        output_ids = model.generate(input_ids, max_length=100, do_sample=True, temperature=0.7)

        # ✅ 생성된 문장 디코딩
        generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return generated_text
    except Exception as e:
        return f"⚠️ KoAlpaca 분석 실패: {str(e)}"

# ✅ 3️⃣ FastAPI 엔드포인트 (구글 팩트체크 + KoAlpaca 결합)
@router.post("/fact-check")
def fact_check(news_request: NewsRequest):
    """팩트체크 API (Google Fact Check API + KoAlpaca 로컬 실행)"""
    try:
        user_query = news_request.content

        # ✅ 1️⃣ 구글 팩트체크 API 결과 확인
        fact_check_result = fact_check_google(user_query)

        if fact_check_result:
            return {
                "message": "Fact-check result found",
                "source": "Google Fact Check API",
                "claims": fact_check_result  # 팩트체크 기관에서 검증한 데이터 반환
            }

        # ✅ 2️⃣ 팩트체크된 데이터가 없으면 KoAlpaca 분석 진행 (로컬 실행)
        koalpaca_analysis = analyze_with_koalpaca(user_query)

        return {
            "message": "Fact-check result not found. KoAlpaca analysis provided.",
            "source": "KoAlpaca (local model)",
            "koalpaca_analysis": koalpaca_analysis  # KoAlpaca의 분석 결과 반환
>>>>>>> 2622a424821b655ee8e8a9ba0e488f99d2f6155f
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fact-checking failed: {str(e)}")

# import os
# import re
# import numpy as np
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
# from konlpy.tag import Okt
# from textblob import TextBlob

# # ✅ FastAPI 라우터 설정
# router = APIRouter()

# # ✅ 모델 경로 설정 (새로 학습한 KoBERT 모델)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "../models/kobert-news-continued")

# # ✅ 라벨 매핑 (0: FAKE, 1: REAL)
# LABELS = {"LABEL_0": "FAKE", "LABEL_1": "REAL"}

# # ✅ KoBERT 모델 로드
# try:
#     tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
#     model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
#     classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model, framework="pt")
# except Exception as e:
#     raise RuntimeError(f"모델 로딩 실패: {str(e)}")

# # ✅ 텍스트 전처리 함수
# okt = Okt()

# def preprocess_text(text):
#     """한글 뉴스 본문 전처리 (불용어 제거 + 형태소 분석)"""
#     text = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)  # 한글만 남기기
#     tokens = okt.morphs(text, stem=True)  # 형태소 분석
#     return " ".join(tokens)

# # ✅ TF-IDF 벡터화기
# vectorizer = TfidfVectorizer(max_features=1000)

# # ✅ 요청 데이터 형식
# class NewsRequest(BaseModel):
#     content: str

# # ✅ 가짜뉴스 판별 API
# @router.post("/predict")
# def predict_news(news_request: NewsRequest):
#     """가짜 뉴스 판별 API"""
#     try:
#         # ✅ 텍스트 전처리 적용
#         processed_text = preprocess_text(news_request.content)

#         # ✅ 감성 분석 점수 추가 (TextBlob)
#         sentiment_score = TextBlob(processed_text).sentiment.polarity

#         # ✅ TF-IDF 기반 키워드 추출
#         tfidf_matrix = vectorizer.fit_transform([processed_text])
#         feature_names = vectorizer.get_feature_names_out()
#         top_keywords = [feature_names[i] for i in tfidf_matrix.toarray()[0].argsort()[-10:]]  # 상위 10개 단어

#         # ✅ KoBERT 모델 예측 (가짜뉴스 판별)
#         result = classifier(processed_text)[0]  
#         label_str = result["label"]  
#         label_name = LABELS.get(label_str, "UNKNOWN")

#         return {
#             "message": "Prediction successful",
#             "label": label_name,  # ✅ "FAKE" 또는 "REAL"
#             "score": result["score"],  # ✅ 신뢰도 점수
#             "processed_text": processed_text,  # ✅ 전처리된 텍스트
#             "top_keywords": top_keywords,  # ✅ 주요 키워드
#             "sentiment_score": sentiment_score  # ✅ 감성 분석 점수 (-1~1)
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
