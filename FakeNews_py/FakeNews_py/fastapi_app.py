from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import save_news_to_db, fetch_all_news
from crawling import get_news_from_naver
import joblib
import logging

app = FastAPI()  # FastAPI 객체 정의

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # 올바른 로거 생성 방식

# 모델 및 벡터라이저 로드
model = joblib.load("lightgbm_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# 요청 데이터 구조 정의
class NewsRequest(BaseModel):
    query: str
    count: int

class NewsData(BaseModel):
    text: str

# 뉴스 가져오기 API
@app.get("/fetch_news")
def fetch_news(query: str, count: int = 10):
    """
    네이버 뉴스 데이터를 가져오는 API
    """
    news_items = get_news_from_naver(query, count)
    if news_items:
        return {"status": "success", "news": news_items}
    else:
        raise HTTPException(status_code=404, detail="뉴스 데이터 가져오기 실패")

# 뉴스 저장 API
@app.post("/save_news")
def save_news(request: NewsRequest):
    """
    네이버 뉴스 데이터를 가져와 데이터베이스에 저장하는 API
    """
    try:
        # 요청 데이터 로그
        logger.info(f"요청 데이터: {request.dict()}")
        
        # 네이버 뉴스 데이터 가져오기
        news_items = get_news_from_naver(request.query, request.count)
        logger.info(f"가져온 뉴스 데이터: {news_items}")
        
        if not news_items:
            raise HTTPException(status_code=404, detail="뉴스 데이터를 가져올 수 없습니다.")
        
        # 뉴스 데이터 저장
        for news in news_items:
            title = news.get("title", "제목 없음")
            description = news.get("description", "내용 없음")
            save_news_to_db(title, description)
            logger.info(f"저장된 뉴스: 제목={title}, 내용={description}")
        
        return {"status": "success", "message": f"{len(news_items)}개 뉴스 저장 완료"}
    except Exception as e:
        logger.error(f"서버 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")

# 데이터베이스에서 모든 뉴스 가져오기
@app.get("/all_news")
def get_all_news():
    """
    데이터베이스에 저장된 모든 뉴스 데이터를 반환
    """
    news_items = fetch_all_news()
    if news_items:
        return {"status": "success", "news": news_items}
    else:
        raise HTTPException(status_code=404, detail="저장된 뉴스 데이터가 없습니다.")

# 가짜 뉴스 판별 API + 로깅 추가
@app.post("/predict")
def predict_news(data: NewsData):
    """
    가짜 뉴스 판별 API
    """
    try:
        # 입력 데이터 로그
        logger.info(f"입력 데이터: {data.text}")
        
        # 예측 로직
        prediction = (model.predict(vectorizer.transform([data.text])) > 0.5).astype(int)[0]
        result = "진짜 뉴스" if prediction == 1 else "가짜 뉴스"
        
        # 예측 결과 로그
        logger.info(f"예측 결과: {result}")
        
        return {"text": data.text, "prediction": result}
    except Exception as e:
        logger.error(f"예측 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"예측 실패: {str(e)}")

# 간단한 데이터 테스트 API
@app.get("/fastapi/data")
def get_data():
    """
    FastAPI 서버 상태 테스트 API
    """
    return {"message": "Hello from FastAPI", "status": "success"}

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)