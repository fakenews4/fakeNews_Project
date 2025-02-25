import requests
import urllib.parse
import pandas as pd
import os
from config.config import get_db_connection,PUBLISHER_MAPPING
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_publisher_from_url(originallink):
    """ 원본 링크에서 도메인을 추출하고 언론사 이름을 반환하는 함수 """
    if not originallink:  # 🔴 `originallink`가 없을 경우 기본값 반환
        return "언론사"

    parsed_url = urlparse(originallink)
    domain = parsed_url.netloc.replace("www.", "")  # `www.` 제거

    return PUBLISHER_MAPPING.get(domain, "지방언론사")  # 매칭 안 되면 `Unknown` 반환

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
        
        # 🔹 제목 또는 설명에 정확한 키워드 포함된 기사만 남김
        filtered_news = []
        for news in news_items:
            title = news["title"]
            description = news["description"]
            
            # 모든 키워드가 포함된 기사만 추가 (부분 포함된 것 제외)
            if all(keyword in title or keyword in description for keyword in keywords):
                filtered_news.append(news)

        print("🔹 [강제 필터링된 뉴스]")
        for news in filtered_news:
            print(f"📰 제목: {news['title']}")
            print(f"📌 설명: {news['description']}")
            print(f"🔗 링크: {news['link']}\n")

        return filtered_news
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
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

def get_random_news_recommendations(keywords):
    conn = get_db_connection()
    
    # 🔹 키워드를 포함하는 기사 검색
    keyword_conditions = " OR ".join([f"title LIKE '%%{keyword}%%'" for keyword in keywords])
    query = f"SELECT * FROM news WHERE {keyword_conditions}"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 🔹 검색된 기사가 없으면 빈 DataFrame 반환
    if df.empty:
        return pd.DataFrame()

    # 🔹 TF-IDF 벡터 변환
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["title"] + " " + df["description"])

    # 🔹 코사인 유사도 계산
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 🔹 평균적으로 유사도가 높은 기사 9개 선택
    avg_similarity = cosine_sim.mean(axis=0)  # 각 기사별 평균 유사도 계산
    df["similarity"] = avg_similarity  # 데이터프레임에 유사도 추가
    df = df.sort_values(by="similarity", ascending=False)  # 유사도가 높은 순으로 정렬

    # 🔹 상위 유사한 기사 중에서 랜덤으로 9개 선택
    top_articles = df.head(20)  # 상위 20개 중에서 랜덤 샘플링
    return top_articles.sample(n=min(9, len(top_articles)))
