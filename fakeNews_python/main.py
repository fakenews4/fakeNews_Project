from fastapi import FastAPI, HTTPException
from handler.proposal import fetch_news_from_api, save_news_to_db, get_random_news_recommendations

app = FastAPI()

@app.get("/news/fetch")
def fetch_news(keywords):
    """
    Fetch news articles from the API based on the given keywords.
    """
    if not keywords:
        raise HTTPException(status_code=400, detail="Keywords are required")

    try:
        news_items = fetch_news_from_api(keywords)
        save_news_to_db(news_items)
        return {"message": "News fetched and saved successfully", "news_count": len(news_items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/news/recommend")
def recommend_news(keywords):
    """
    Recommend random news articles based on the given keywords.
    """
    if not keywords:\
        raise HTTPException(status_code=400, detail="Keywords are required")

    try:
        recommended_news = get_random_news_recommendations(keywords)
        if recommended_news.empty:
            return {"message": "No related news found."}

        recommendations = []
        for idx, row in recommended_news.iterrows():
            recommendations.append({
                "title": row["title"],
                "link": row["link"],
                "description": row["description"],
            })

        return {"message": "Recommendations found", "news": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    