import asyncio
import ollama
from fastapi import HTTPException

async def summarize_content(content: str):
    try:
        print("요약 시작...")  # 요약 시작 로그

        summarize_question = f"다음 내용을 요약해 주세요: {content}"

        # 비동기적으로 요약 요청 처리
        response = await asyncio.to_thread(
            ollama.chat,
            model='gemma2',
            messages=[
                {"role": "system", "content": "당신은 유용한 한국어 챗봇입니다."},
                {"role": "user", "content": summarize_question}
            ]
        )

        print("응답을 받았습니다...")  # 응답 수신 후 로그

        if "message" not in response:
            raise HTTPException(status_code=500, detail="Ollama 응답 오류")
        
        print("응답 처리 중...")  # 응답 처리 중 로그
        summary = response["message"]

        print("요약 완료.")  # 요약 완료 로그
        return {"summary": summary}

    except Exception as e:
        print(f"오류 발생: {str(e)}")  # 오류 발생 시 로그
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")