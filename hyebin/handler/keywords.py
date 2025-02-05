from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
from collections import Counter
from konlpy.tag import Okt

okt = Okt()

async def extract_keywords_from_content(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="웹 페이지 요청 실패")
        
        soup = BeautifulSoup(response.content, 'html.parser')

        for img in soup.find_all('img'):
            img.decompose()
        for figcaption in soup.find_all('figcaption'):
            figcaption.decompose()
        for span in soup.find_all('span', title=True):
            span.decompose()

        article_content = ""
        for tag in ["article"]:
            for element in soup.find_all(tag):
                article_content += element.get_text(separator=" ") + " "

        if not article_content.strip():
            raise HTTPException(status_code=500, detail="크롤링된 콘텐츠가 없습니다.")

        keywords = extract_keywords(article_content, top_n=1)
        return {"keywords": keywords}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")

async def extract_keywords_from_text(data: dict):
    content = data.get("content", "").strip()
    if not content:
        raise HTTPException(status_code=400, detail="추출할 텍스트가 없습니다.")

    keywords = extract_keywords(content, top_n=1)
    return {"success": True, "keywords": keywords}

def extract_keywords(text, top_n=1):
    words = okt.pos(text)
    all_nouns = [word for word, pos in words if pos in ['Nnp', 'Noun'] and len(word) > 1]

    word_counts = Counter(all_nouns)
    return [word for word, _ in word_counts.most_common(top_n)] or ["키워드 없음"]
