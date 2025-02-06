import requests
import re

# 텍스트 전처리 함수
def clean_text(text):
    """
    불필요한 텍스트 제거하는 함수
    """
    text = re.sub(r"<[^>]+>", "", text)  # HTML 태그 제거
    text = re.sub(r"\n+", " ", text)  # 줄 바꿈 제거
    text = re.sub(r"(구독|저작권|All rights reserved|추천 요소).*", "", text)  # 특정 키워드 제거
    text = re.sub(r"\s+", " ", text).strip()  # 공백 정리
    return text

# 네이버 뉴스 API를 사용하여 뉴스 데이터를 가져오는 함수
def get_news_from_naver(query, display=10):
    """
    네이버 뉴스 API를 통해 뉴스 데이터를 가져옵니다.
    :param query: 검색할 키워드
    :param display: 가져올 뉴스 개수 (최대 100개)
    :return: 뉴스 데이터 리스트
    """
    # 네이버 API 키
    CLIENT_ID = "iRIOTQyt9HupORq9qx6K"
    CLIENT_SECRET = "GsjXOBKZgw"

    # API URL 및 요청 헤더
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "date"  # 정렬 기준: 최신순
    }

    # API 요청
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        news_items = response.json().get("items", [])
        # 전처리: 불필요한 텍스트 제거
        for news in news_items:
            news["title"] = clean_text(news.get("title", ""))
            news["description"] = clean_text(news.get("description", ""))
        return news_items
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패: {e}")
        return []

# 테스트 코드
if __name__ == "__main__":
    # 테스트용 키워드
    query = "AI"
    news = get_news_from_naver(query, display=5)

    if news:
        for i, item in enumerate(news):
            print(f"{i + 1}. 제목: {item['title']}\n링크: {item['link']}\n설명: {item['description']}\n")
    else:
        print("뉴스 데이터를 가져오는 데 실패했습니다.")
