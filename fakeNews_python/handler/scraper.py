import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import tensorflow as tf

# ✅ Google AI API 설정 (API Key 필요)
genai.configure(api_key="AIzaSyAqiutR9Uc1Q4DUtRQdiAu58U6apM8jmek")  # 발급받은 API 키 입력

def summarize_news(text):
    """Google Gemini AI를 사용하여 뉴스 내용을 요약하는 함수"""
    model = genai.GenerativeModel("gemini-pro")  # Gemini 모델 선택
    response = model.generate_content(f"다음 뉴스를 300자 이하로 요약해줘:\n\n{text}")
    return response.text  # 요약된 뉴스 반환

def scrape_naver_article(url: str):
    """
    네이버 뉴스 기사 본문 크롤링 및 요약 기능 추가
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        print(f"🛠️ 네이버 뉴스 크롤링 시작: {url}")

        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ 본문 크롤링 (네이버 뉴스 구조 반영)
        article_body = soup.find("article", id="dic_area")
        if not article_body:
            return {"error": "❌ 네이버 뉴스 본문을 찾을 수 없습니다."}

        content_text = "\n".join(article_body.stripped_strings).strip()
        if not content_text:
            return {"error": "❌ 크롤링된 본문이 비어 있습니다."}

        print(f"✅ 네이버 뉴스 크롤링 성공\n본문: {content_text[:100]}...")

        # ✅ 요약 기능 추가
        summary = summarize_news(content_text)
        print(f"✅ 뉴스 요약 완료: {summary[:100]}...")

        return {"content": content_text, "summary": summary}

    except Exception as e:
        print(f"❌ 네이버 뉴스 크롤링 오류: {e}")
        return {"error": str(e)}