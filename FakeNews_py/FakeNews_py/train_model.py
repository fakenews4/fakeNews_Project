# 데이터 전처리(텍스트 클렌징, TF-IDF 변환)
# LightGBM 모델 학습 및 저장

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import joblib
from database import fetch_all_news

# 1. 데이터 로드
data = fetch_all_news()  # 데이터베이스에서 뉴스 데이터 가져오기
df = pd.DataFrame(data)

# 데이터 전처리 함수
def clean_text(text):
    """
    텍스트 전처리 함수: HTML 태그 제거, 특수 문자 제거, 공백 정리
    """
    text = re.sub(r"<[^>]+>", "", text)  # HTML 태그 제거
    text = re.sub(r"[^a-zA-Z가-힣0-9\s]", "", text)  # 특수 문자 제거
    text = re.sub(r"\s+", " ", text).strip()  # 공백 정리
    return text

# 데이터 전처리
df["text"] = (df["title"] + " " + df["content"]).apply(clean_text)  # 제목과 내용을 병합 후 전처리

# 레이블 생성 (임시로 1과 0 반복)
df["label"] = [1 if i % 2 == 0 else 0 for i in range(len(df))]  # 데이터 길이에 맞게 생성

# 2. TF-IDF 변환
vectorizer = TfidfVectorizer(max_features=5000)  # 최대 5000개의 특징 선택
X = vectorizer.fit_transform(df["text"])  # 텍스트 데이터를 TF-IDF로 변환
y = df["label"]  # 레이블 데이터

# 학습 및 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 학습 데이터 및 테스트 데이터 확인
print("Train Data Shape:", X_train.shape)
print("Test Data Shape:", X_test.shape)

# 3. LightGBM 데이터셋 생성
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test)

# 4. LightGBM 모델 학습
params = {
    "objective": "binary",  # 이진 분류
    "boosting_type": "gbdt",  # Gradient Boosting
    "metric": "binary_error",  # 평가 메트릭: 이진 분류 오류율
    "num_leaves": 31,  # 리프 노드 수
    "learning_rate": 0.05,  # 학습 속도
    "feature_fraction": 0.9,  # 사용할 피처의 비율
}

# 학습 진행 상황 출력 구현
def print_eval_result(epoch, result):
    """
    LightGBM 학습 진행 상황 출력
    """
    print(f"Epoch {epoch}: Validation Binary Error = {result['binary_error']}")

# 모델 학습
model = lgb.train(
    params,
    train_data,
    num_boost_round=100,  # 부스팅 라운드 수
    valid_sets=[test_data],  # Validation 데이터 설정
    valid_names=["validation"],  # Validation 데이터 이름
)

# 5. 모델 및 벡터라이저 저장
joblib.dump(model, "lightgbm_model.pkl")  # 학습된 LightGBM 모델 저장
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")  # TF-IDF 벡터라이저 저장
print("모델 및 벡터라이저 저장 완료!")
