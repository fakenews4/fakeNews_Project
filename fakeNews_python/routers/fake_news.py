import os
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline

# ✅ 뉴스 판별 API 라우터 설정
router = APIRouter()

# ✅ 모델 경로 설정 (새로 학습한 KoBERT 모델)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/kobert-news-finetuned")

# ✅ 라벨 매핑 (0: FAKE, 1: REAL)
LABELS = {"LABEL_0": "FAKE", "LABEL_1": "REAL"}

# ✅ 모델 로드
try:
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model, framework="pt")
except Exception as e:
    raise RuntimeError(f"모델 로딩 실패: {str(e)}")

# ✅ 요청 데이터 형식
class NewsRequest(BaseModel):
    content: str

# ✅ 뉴스 판별 API
@router.post("/news/predict")
def predict_news(news_request: NewsRequest):
    """가짜 뉴스 판별 API"""
    try:
        result = classifier(news_request.content)[0]  # ✅ 첫 번째 결과 사용
        label_str = result["label"]  # ✅ "LABEL_0" 또는 "LABEL_1"
        label_name = LABELS.get(label_str, "UNKNOWN")  # ✅ 매핑된 값 가져오기

        return {
            "message": "Prediction successful",
            "label": label_name,  # ✅ "FAKE" 또는 "REAL"
            "score": result["score"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
