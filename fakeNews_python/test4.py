from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# 모델 및 토크나이저 로드
MODEL_NAME = "D:/fakeNews_Project/fakeNews_python/models/us_fake_news_model4"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# 파이프라인 생성
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# 테스트할 뉴스 기사
article = """In a shocking development, House Speaker Nancy Pelosi has been arrested for treason by U.S. military forces in a secret sting operation.
Sources inside the Pentagon confirm that Pelosi was taken into custody after evidence surfaced showing her involvement in an underground plot to overthrow the Trump administration.
The operation, conducted in coordination with military intelligence, reportedly uncovered documents linking Pelosi to foreign governments and election fraud efforts.
Although mainstream media refuses to report on the story, insiders claim that Pelosi is currently being held at a classified military facility, awaiting trial under martial law."""

# 예측
result = classifier(article)
print(result)
