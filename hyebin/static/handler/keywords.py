from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
from collections import Counter
from konlpy.tag import Okt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 형태소 분석기 (한국어)
okt = Okt()

# NLTK 관련 리소스 다운로드
nltk.download('punkt_tab')
nltk.download('stopwords')

try:
    stop_words_en = set(stopwords.words('english'))  # 영어 불용어 리스트
except Exception as e:
    stop_words_en = set()  # 예외 발생 시 빈 집합으로 설정

async def extract_keywords_from_content(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="웹 페이지 요청 실패")
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # 불필요한 요소 제거
        for tag in ["img", "figcaption", "script", "style", "iframe"]:
            for elem in soup.find_all(tag):
                elem.decompose()

        # 기사 내용 추출 (article 태그만 사용)
        article_content = " ".join([element.get_text(separator=" ") for element in soup.find_all("article")])

        article_content = article_content.strip()
        if not article_content:
            raise HTTPException(status_code=500, detail="크롤링된 콘텐츠가 없습니다.")

        # 언어 감지 및 키워드 추출
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

def extract_keywords(text, top_n=5):
    if not text.strip():
        return ["키워드 없음"]

    # 언어 감지: 한글 포함 여부 확인
    is_korean = any("\uAC00" <= char <= "\uD7A3" for char in text)

    try:
        if is_korean:
            # ✅ 한국어 뉴스 처리 (Okt 사용)
            words_ko = okt.pos(text)
            all_nouns = [word for word, pos in words_ko if pos in ['Nnp', 'Noun'] and len(word) > 1]
        else:
            # ✅ 영어 뉴스 처리 (nltk 사용)
            words_en = word_tokenize(text)
            all_nouns = [word.lower() for word in words_en if word.isalpha() and word.lower() not in stop_words_en]

    except Exception as e:
        print(f"❌ 키워드 추출 오류: {e}")
        return ["키워드 추출 실패"]

    # 키워드 빈도수 계산
    word_counts = Counter(all_nouns)
    return [word for word, _ in word_counts.most_common(top_n)] or ["키워드 없음"]
