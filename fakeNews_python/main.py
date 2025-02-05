from fastapi import FastAPI, HTTPException
from handler.proposal import fetch_news_from_api, save_news_to_db, get_random_news_recommendations

app = FastAPI()

@app.get("/news/recommend")
def fetch_and_recommend_news(keywords: str):
    if not keywords:
        keywords = "korea"

    try:
        # Step 1: Fetch news from API
        news_items = fetch_news_from_api(keywords)
        if not news_items:
            return {"message": "No news found for the given keywords."}

        # Step 2: Save news to database
        save_news_to_db(news_items)

        # Step 3: Get recommendations from the saved news
        recommended_news = get_random_news_recommendations(keywords)
        if recommended_news.empty:
            return {"message": "News fetched and saved, but no recommendations found."}

        recommendations = []
        for _, row in recommended_news.iterrows():
            recommendations.append({
                "title": row["title"],
                "link": row["link"],
                "description": row["description"],
                "publisher": row.get("publisher", "Unknown"),  # ✅ 언론사 정보 포함
            })

        return {
            "message": "News fetched, saved, and recommendations generated successfully",
            "news_count": len(news_items),
            "news": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

