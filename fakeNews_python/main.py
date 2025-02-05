from fastapi import FastAPI
from routers import news  # ✅ routers 폴더에서 news 모듈 가져오기

app = FastAPI()

# ✅ 라우트 등록 (모든 API가 `/api/...`로 접근 가능)
app.include_router(news.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}