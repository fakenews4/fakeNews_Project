from transformers import pipeline

# 모델 로드
MODEL_NAME = "D:/fakeNews_Project/fakeNews_python/models/us_fake_news_model5"
classifier = pipeline("text-classification", model=MODEL_NAME, tokenizer=MODEL_NAME)

# 테스트할 뉴스 기사
article = """I apologize for any confusion caused by previous responses. It appears there was an error in the information provided earlier. To clarify, as of February 12, 2025, there have been no official announcements or actions regarding the imposition of 25% tariffs on steel and aluminum imports by the U.S. government. Any such reports are inaccurate. If you have any other topics or need information on different subjects, feel free to ask!"""

# 예측
result = classifier(article)
print(result)
