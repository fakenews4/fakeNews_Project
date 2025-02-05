# 데이터 모델 정의(선택) TF-IDF + LightGRM 학습 코드 및 모델 저장 / 로드 코드 작성
from sklearn.feature_extraction.text import TfidfVectorizer
from lightgbm import LGBMClassifier
import pickle

def train_model(data):
    # 전처리 및 벡터화
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(data['content_clean'])
    y = data['label']
    
    # 모델 학습
    model = LGBMClassifier()
    model.fit(X, y)
    
    # 모델 및 벡터라이저 저장
    with open("tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("fake_news_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("모델 학습 및 저장 완료")