import requests

# 네이버 뉴스 API를 사용하여 뉴스 데이터를 가져오는 함수
def get_news_from_naver(query, display=10):
    """
    네이버 뉴스 API를 통해 뉴스 데이터를 가져옵니다.
    :param query: 검색할 키워드
    :param display: 가져올 뉴스 개수 (최대 100개)
    :return: 뉴스 데이터 리스트
    """
    # 네이버 API 키 (발급받은 키를 여기에 입력하세요)
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
        return response.json().get("items", [])
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
            print(f"{i + 1}. 제목: {item['title']}\n링크: {item['link']}\n")
