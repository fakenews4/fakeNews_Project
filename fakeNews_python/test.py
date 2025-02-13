from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

def load_model(model_path):
    # 로컬에 저장된 모델 로드
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
    
    # 텍스트 분류 파이프라인 생성
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return classifier

def predict_fake_news(classifier, text):
    result = classifier(text)
    return result

if __name__ == "__main__":
    # 로컬 모델 경로
    model_path = "D:/fakeNews_Project/fakeNews_python/models/us_fake_news_model"  # 로컬에 저장된 모델 폴더 경로
    
    print("🚀 로컬 모델을 불러오는 중...")
    classifier = load_model(model_path)
    print("✅ 모델 로드 완료!")
    
    # 테스트할 뉴스 기사 입력
    articles = [
        """During the 2016 U.S. presidential election, a conspiracy theory falsely claimed that a child trafficking ring involving Democratic candidate Hillary Clinton was operating out of the Comet Ping Pong pizzeria in Washington, D.C. This baseless allegation led to threats against the restaurant and culminated in an armed individual entering the establishment to "investigate," endangering patrons and staff.""",
        """ During the 2016 U.S. presidential election, a fake news website published an article claiming that Pope Francis had endorsed Donald Trump for president.
The article falsely stated that the Pope had declared Trump "a true defender of Christian values" in an interview.
This fake news story went viral on Facebook and other social media platforms, gaining millions of shares.
However, the Vatican immediately denied the claim, and fact-checking organizations confirmed that the story was entirely fabricated. """,
        "Aliens have landed in California and are communicating with humans!",
        "Fake News Alert: A new virus is spreading through WiFi signals!"
    ]
    
    print("\n🔍 가짜 뉴스 판별 결과:")
    for article in articles:
        prediction = predict_fake_news(classifier, article)
        print(f"📰 기사: {article}\n🔍 예측 결과: {prediction}\n")
