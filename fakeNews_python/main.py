from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news, crawler
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

print("✅ FastAPI 서버 시작 중...")

app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ✅ 라우터 추가
app.include_router(news.router)
app.include_router(crawler.router)


print("✅ FastAPI 서버가 정상적으로 실행되었습니다!")

