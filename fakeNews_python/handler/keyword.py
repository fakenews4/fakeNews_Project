import re
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    """ 한글과 공백을 제외한 모든 문자 제거 """
    text = re.sub(r"[^가-힣\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_keywords(text):
    """
    형태소 분석(Okt) + TF-IDF를 활용한 한국어 키워드 추출 (가장 중요한 1개만)
    :param text: 기사 본문
    :return: 가장 중요한 키워드 (1개)
    """
    try:
        # ✅ 본문이 너무 짧으면 분석 불가능
        if len(text) < 20:
            return "본문이 너무 짧음"

        # ✅ 텍스트 전처리
        text = clean_text(text)

        # ✅ 형태소 분석기 초기화
        okt = Okt()
        nouns = okt.nouns(text)  # 명사만 추출

        # ✅ 명사가 없으면 기본값 반환
        if not nouns:
            return "키워드 없음"

        # ✅ TF-IDF를 이용한 키워드 추출
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([" ".join(nouns)])  # 명사 리스트를 공백으로 연결하여 벡터화
        scores = dict(zip(vectorizer.get_feature_names_out(), X.toarray().flatten()))

        # ✅ TF-IDF 점수가 가장 높은 키워드 선택
        if scores:
            best_keyword = max(scores, key=scores.get)
            return best_keyword
        else:
            return "키워드 없음"

    except Exception as e:
        print(f"❌ 키워드 추출 오류: {e}")
        return "키워드 추출 실패"
