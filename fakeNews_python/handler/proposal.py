import requests
import urllib.parse
import pandas as pd
import os
from config.config import get_db_connection,PUBLISHER_MAPPING
from urllib.parse import urlparse

def get_publisher_from_url(originallink):
    """ 원본 링크에서 도메인을 추출하고 언론사 이름을 반환하는 함수 """
    if not originallink:  # 🔴 `originallink`가 없을 경우 기본값 반환
        return "언론사"

    parsed_url = urlparse(originallink)
    domain = parsed_url.netloc.replace("www.", "")  # `www.` 제거

    return PUBLISHER_MAPPING.get(domain, "지방언론사")  # 매칭 안 되면 `Unknown` 반환

# API 호출: 키워드를 기반으로 뉴스 가져오기
def fetch_news_from_api(keywords, display=100):
    client_id = os.getenv("NAVER_KEY")
    client_secret = os.getenv("NAVER_SECRET_KEY")

    query = " OR ".join(keywords)
    encoded_query = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display={display}"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        news_items = response.json().get("items", [])

        for news in news_items:
            originallink = news.get("originallink", news.get("link", ""))
            news["publisher"] = get_publisher_from_url(originallink)  # ✅ 언론사 정보 추가

        return news_items
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# DB에 중복 확인 및 뉴스 저장
def save_news_to_db(news_items):
    conn = get_db_connection()
    cursor = conn.cursor()

    for news in news_items:
        title = news["title"]
        publisher = news.get("publisher", "언론사")  # ✅ 언론사 정보 추가

        # 중복 검사: 같은 제목의 기사가 DB에 있는지 확인
        cursor.execute("SELECT COUNT(*) FROM news WHERE title = %s", (title,))
        if cursor.fetchone()[0] == 0:
            # 중복되지 않은 경우만 저장
            cursor.execute("""
            INSERT INTO news (title, link, description, publisher, category)
            VALUES (%s, %s, %s, %s, %s)
            """, (
                title,
                news["link"],
                news["description"],
                publisher,  # ✅ `publisher` 저장
                "general"
            ))

    conn.commit()
    conn.close()

# DB에서 9개의 뉴스 가져오기
def get_news_recommendations():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM news LIMIT 9", conn)
    conn.close()
    return df

# DB에서 키워드와 관련된 기사 9개 랜덤 선택
def get_random_news_recommendations(keywords):
    conn = get_db_connection()
    
    # 키워드를 포함하는 기사를 검색
    keyword_conditions = " OR ".join([f"title LIKE '%%{keyword}%%'" for keyword in keywords])
    query = f"SELECT * FROM news WHERE {keyword_conditions}"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 기사가 없으면 빈 DataFrame 반환
    if df.empty:
        return pd.DataFrame()

    # 기사가 9개 이상이면 랜덤으로 9개 선택
    return df.sample(n=min(9, len(df)))
