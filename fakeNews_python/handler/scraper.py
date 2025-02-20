import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# ✅ 한국어 뉴스 요약 모델 (KoBART 기반)
summarizer = pipeline(
    "summarization",
    model="ainize/kobart-news",
    tokenizer="ainize/kobart-news"
)

def scrape_naver_article(url: str):
    """
    네이버 뉴스 기사 본문 크롤링 후 KoBART 모델로 요약
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

        # ✅ 입력 길이 제한 (1024자 이하)
        trimmed_text = content_text[:1024]

        # ✅ 본문이 충분히 길 때만 요약 실행 (300자 이상)
        if len(trimmed_text) > 300:
            try:
                summary = summarizer(trimmed_text, max_length=300, min_length=150, do_sample=False)
                summarized_text = summary[0]['summary_text']
            except Exception as e:
                return {"error": f"❌ 요약 중 오류 발생: {str(e)}"}
        else:
            summarized_text = trimmed_text  # 300자 이하면 원본 그대로 사용

        print(f"✅ 네이버 뉴스 크롤링 및 요약 성공\n요약: {summarized_text[:100]}...")
        return {"content": summarized_text}

    except Exception as e:
        print(f"❌ 네이버 뉴스 크롤링 오류: {e}")
        return {"error": str(e)}
