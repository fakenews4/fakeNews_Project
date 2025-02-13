from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# 사용할 모델 (추가 학습 없이 바로 사용 가능)
MODEL_NAME = "D:/fakeNews_Project/fakeNews_python/models/us_fake_news_model3"

# 모델 및 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# 텍스트 분류 파이프라인 생성
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# 테스트할 뉴스 기사 리스트
articles = [
    """On January 6, 2021, the U.S. Congress officially certified Joe Biden as the winner of the 2020 presidential election.
Despite objections from some lawmakers and a violent attack on the U.S. Capitol earlier that day, the certification process was completed in the early hours of January 7, 2021.
Vice President Mike Pence presided over the joint session of Congress, confirming that Biden had won 306 electoral votes against Donald Trump’s 232 votes.
The certification formally confirmed that Biden would be inaugurated as the 46th president of the United States on January 20, 2021.""",
    """A new investigative report reveals that former President Barack Obama has been secretly funding a shadow government to overthrow Donald Trump.
Anonymous sources claim that Obama has been directing millions of dollars to left-wing activists and deep-state operatives who are working behind the scenes to sabotage Trump’s presidency.
The report suggests that a hidden network of former intelligence officials and media insiders are coordinating efforts to undermine the Trump administration.
While mainstream media refuses to cover this scandal, many believe this is the biggest political conspiracy in modern U.S. history."""
]
# 뉴스 기사 판별 결과 출력
print("\n🔍 Fake News Detection Results:\n")
for article in articles:
    result = classifier(article)
    label = result[0]['label']
    score = result[0]['score']
    
    print(f"📰 Article: {article}\n🔍 Prediction: {label} (Confidence: {score:.2f})\n")
