import os
import re
import numpy as np
import kss
import requests
from transformers import pipeline

def classify_long_text(text):
    """한국어 문장 기준으로 청크 분리 후 가짜 뉴스 판별"""
    fake_news_classifier = pipeline("text-classification", model="beomi/kcbert-base", tokenizer="beomi/kcbert-base")

    sentences = kss.split_sentences(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < 1000:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    results = []
    for chunk in chunks:
        try:
            result = fake_news_classifier(chunk)
            score = result[0]['score']
            adjusted_score = adjust_score(score, check_fake_news_indicators(chunk))
            results.append(adjusted_score)
        except Exception as e:
            print(f"❌ 가짜 뉴스 판별 오류: {e}")
            continue

    avg_score = np.mean(results) if results else 0.5
    final_label = 'FAKE' if avg_score > 0.6 else 'REAL'
    return {"label": final_label, "score": avg_score}

def check_fake_news_indicators(text):
    """가짜뉴스 특성 체크"""
    indicators = {
        'excessive_punctuation': len(re.findall(r'[!?]{2,}', text)) > 0,
        'sensational_words': any(word in text.lower() for word in [
            '충격', '경악', '발칵', '화들짝', '헉', '대박', '전격', '특종', '단독'
        ]),  
        'unverified_sources': any(phrase in text for phrase in [
            '카더라', '라고 한다', '전해졌다', '소식통'
        ])
    }
    return indicators

def adjust_score(base_score, indicators):
    """지표에 따른 신뢰도 조정"""
    score = base_score
    if indicators['excessive_punctuation']:
        score += 0.1
    if indicators['sensational_words']:
        score += 0.15
    if indicators['unverified_sources']:
        score += 0.15
    return min(max(score, 0), 1)

def analyze_with_gemini(article):
    """Gemini API를 사용한 분석"""
    gemini_api_key = os.getenv("GEMINI_API")  
    if not gemini_api_key:
        return "Gemini API 키가 설정되지 않았습니다."

    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        headers = {'Content-Type': 'application/json', 'x-goog-api-key': gemini_api_key}
        
        prompt = (
            "다음 뉴스 기사의 진위 여부를 분석해주세요. 다음 항목별로 평가해주세요:\n"
            "1. 기사의 객관성\n"
            "2. 사실 확인 가능한 정보의 존재 여부\n"
            "3. 감정적 표현이나 과장된 표현의 사용\n"
            "4. 출처와 인용의 명확성\n\n"
            f"기사 내용:\n{article}"
        )

        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "분석 결과 없음")
    
    except Exception as e:
        return f"Gemini 분석 중 오류 발생: {str(e)}"

def classify_news(article):
    """전체 뉴스 분석"""
    if not article or len(article.strip()) == 0:
        return {"error": "분석할 텍스트를 입력해주세요."}

    try:
        # ✅ 1️⃣ 가짜 뉴스 판별
        fake_news_result = classify_long_text(article)
        credibility_score = (1 - float(fake_news_result["score"])) * 100
        is_fake = credibility_score < 40

        # ✅ 2️⃣ Gemini 추가 분석
        gemini_analysis = analyze_with_gemini(article)

        return {
            "label": "FAKE" if is_fake else "REAL",
            "credibility_score": round(credibility_score, 2),
            "gemini_analysis": gemini_analysis
        }

    except Exception as e:
        return {"error": f"분석 중 오류 발생: {str(e)}"}
