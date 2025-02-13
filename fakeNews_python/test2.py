from transformers import pipeline

# 사용할 모델 (추가 학습 없이 사용 가능)
MODEL_NAME = "D:/fakeNews_Project/fakeNews_python/models/us_fake_news_model2"

# 텍스트 분류 파이프라인 로드
classifier = pipeline("text-classification", model=MODEL_NAME, tokenizer=MODEL_NAME)

# 테스트할 뉴스 기사 리스트
articles = [
    """On November 7, 2020, major U.S. news networks projected that Joe Biden had won the 2020 U.S. presidential election, defeating incumbent Donald Trump.
Biden secured over 270 electoral votes, making him the 46th president of the United States.
His running mate, Kamala Harris, also made history as the first female, first Black, and first South Asian vice president.
Despite legal challenges and claims of election fraud from the Trump campaign, the results were certified by all states and affirmed by the U.S. Congress on January 6, 2021.""",
    """A breaking report claims that former President Donald Trump has declared martial law to overturn the 2020 U.S. presidential election results.
Sources inside the White House reveal that Trump has ordered the military to seize voting machines and re-run the election in key swing states.
The report also suggests that Trump has refused to leave office and is planning to stay in power despite losing the election.
Supporters claim that this move is necessary to "stop the steal," but legal experts warn that it would be an unconstitutional power grab."""
]

# 뉴스 기사 판별 결과 출력
print("\n🔍 Fake News Detection Results:\n")
for article in articles:
    result = classifier(article)
    label = result[0]['label']
    score = result[0]['score']
    
    print(f"📰 Article: {article}\n🔍 Prediction: {label} (Confidence: {score:.2f})\n")
