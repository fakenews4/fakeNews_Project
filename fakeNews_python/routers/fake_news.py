import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

# ✅ FastAPI 라우터 설정
router = APIRouter()

# ✅ KcELECTRA 모델 경로 설정
MODEL_PATH = os.path.join("D:/fakeNews_Project/fakeNews_python/models/kcelectra-news-finetuned")

# ✅ 라벨 매핑 (0: FAKE, 1: REAL)
LABELS = {"LABEL_0": "FAKE", "LABEL_1": "REAL"}  # KcELECTRA의 라벨과 동일한지 확인 필요

# ✅ KcELECTRA 모델 로드
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model, framework="pt")
except Exception as e:
    raise RuntimeError(f"모델 로딩 실패: {str(e)}")

# ✅ 요청 데이터 형식
class NewsRequest(BaseModel):
    content: str

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
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
