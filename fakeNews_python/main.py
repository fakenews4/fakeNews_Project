from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from routers import news, fake_news, main_news

print("✅ FastAPI 서버 시작 중...")

app = FastAPI()

# ✅ CORS 설정 추가 (FastAPI 객체에서 해야 함)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ✅ 정적 파일 서빙 설정 (FastAPI 객체에서 해야 함)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ✅ 라우터 추가
app.include_router(main_news.router)  # main_news에서 기능 엔드포인트 관리
app.include_router(news.router)
# app.include_router(fake_news.router)

@app.get("/")
async def read_root():
    file_path = os.path.join(os.getcwd(), "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)

print("✅ FastAPI 서버가 정상적으로 실행되었습니다!")


