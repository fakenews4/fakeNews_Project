from fastapi import FastAPI
from routers import news, fake_news  # ✅ 라우터 추가

print("✅ FastAPI 서버 시작 중...")  # ✅ 서버 시작 확인 로그

app = FastAPI()

app.include_router(news.router)
app.include_router(fake_news.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

print("✅ FastAPI 서버가 정상적으로 실행되었습니다!")  # ✅ 실행 완료 확인 로그
