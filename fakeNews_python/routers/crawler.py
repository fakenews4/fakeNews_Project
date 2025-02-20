from fastapi import APIRouter, HTTPException
from handler.scraper import scrape_naver_article
from handler.models import classify_news

router = APIRouter()

@router.get("/api/crawler")
async def fetch_and_analyze_news(url: str):
    """
    뉴스 URL을 받아서 크롤링 후 AI 모델로 분석하여 가짜 뉴스 여부를 판별
    """
    try:
        # ✅ 1️⃣ 뉴스 크롤링 실행
        result = scrape_naver_article(url)
        if not result or "error" in result:
            raise HTTPException(status_code=404, detail="기사 정보를 가져올 수 없습니다.")

        content = result.get("content", "")

        # ✅ 2️⃣ AI 모델 판별 실행
        analysis_result = classify_news(content)

        # ✅ 3️⃣ 최종 결과 반환
        return {
            "content": content,
            "analysis": analysis_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
