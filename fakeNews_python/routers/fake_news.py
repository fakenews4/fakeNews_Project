import os
import re
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
from textblob import TextBlob

# ✅ FastAPI 라우터 설정
router = APIRouter()

# ✅ 모델 경로 설정 (새로 학습한 KoBERT 모델)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/kobert-news-continued")

# ✅ 라벨 매핑 (0: FAKE, 1: REAL)
LABELS = {"LABEL_0": "FAKE", "LABEL_1": "REAL"}

# ✅ KoBERT 모델 로드
try:
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model, framework="pt")
except Exception as e:
    raise RuntimeError(f"모델 로딩 실패: {str(e)}")

# ✅ 텍스트 전처리 함수
okt = Okt()

def preprocess_text(text):
    """한글 뉴스 본문 전처리 (불용어 제거 + 형태소 분석)"""
    text = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)  # 한글만 남기기
    tokens = okt.morphs(text, stem=True)  # 형태소 분석
    return " ".join(tokens)

# ✅ TF-IDF 벡터화기
vectorizer = TfidfVectorizer(max_features=1000)

# ✅ 요청 데이터 형식
class NewsRequest(BaseModel):
    content: str

# ✅ 가짜뉴스 판별 API
@router.post("/predict")
def predict_news(news_request: NewsRequest):
    """가짜 뉴스 판별 API"""
    try:
        # ✅ 텍스트 전처리 적용
        processed_text = preprocess_text(news_request.content)

        # ✅ 감성 분석 점수 추가 (TextBlob)
        sentiment_score = TextBlob(processed_text).sentiment.polarity

        # ✅ TF-IDF 기반 키워드 추출
        tfidf_matrix = vectorizer.fit_transform([processed_text])
        feature_names = vectorizer.get_feature_names_out()
        top_keywords = [feature_names[i] for i in tfidf_matrix.toarray()[0].argsort()[-10:]]  # 상위 10개 단어

        # ✅ KoBERT 모델 예측 (가짜뉴스 판별)
        result = classifier(processed_text)[0]  
        label_str = result["label"]  
        label_name = LABELS.get(label_str, "UNKNOWN")

        return {
            "message": "Prediction successful",
            "label": label_name,  # ✅ "FAKE" 또는 "REAL"
            "score": result["score"],  # ✅ 신뢰도 점수
            "processed_text": processed_text,  # ✅ 전처리된 텍스트
            "top_keywords": top_keywords,  # ✅ 주요 키워드
            "sentiment_score": sentiment_score  # ✅ 감성 분석 점수 (-1~1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
