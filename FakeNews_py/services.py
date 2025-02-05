# 서비스 계층(비즈니스 로직) (선택) / 데이터 전처리(텍스트 정제, TF-IDF 변환 등) 및 모델 예측 코드 작성
import re
import pickle

# 텍스트 전처리 함수
def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)  # HTML 태그 제거
    text = re.sub(r'\W+', ' ', text)     # 특수 문자 제거
    text = text.lower()                  # 소문자 변환
    return text

# 모델 및 벡터라이저 로드
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("fake_news_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_article(article):
    # 전처리 및 벡터화
    clean_article = clean_text(article)
    article_tfidf = vectorizer.transform([clean_article])
    
    # 예측
    prediction = model.predict(article_tfidf)
    return "진짜 뉴스" if prediction[0] == 1 else "가짜 뉴스"
