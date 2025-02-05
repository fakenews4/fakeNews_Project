from fastapi import FastAPI
from pydantic import BaseModel
from database import save_news_to_db, fetch_all_news
from crawling import get_news_from_naver

app = FastAPI()  # FastAPI 객체 정의

# 뉴스 데이터 요청 구조 정의
class NewsRequest(BaseModel):
    query: str
    count: int = 10

# 뉴스 가져오기 API
@app.get("/fetch_news")
def fetch_news(query: str, count: int = 10):
    news_items = get_news_from_naver(query, count)
    if news_items:
        return {"status": "success", "news": news_items}
    else:
        return {"status": "error", "message": "뉴스 데이터 가져오기 실패"}

# 뉴스 저장 API
@app.post("/save_news")
def save_news(query: str, count: int = 10):
    news_items = get_news_from_naver(query, count)
    if news_items:
        for news in news_items:
            save_news_to_db(news["title"], news["description"])
        return {"status": "success", "message": f"{len(news_items)}개 뉴스 저장 완료"}
    else:
        return {"status": "error", "message": "뉴스 데이터 가져오기 실패"}

# 간단한 데이터 테스트 API
@app.get("/fastapi/data")
def get_data():
    return {"message": "Hello from FastAPI", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
