import asyncio
import ollama
from fastapi import HTTPException  # FastAPI에서 HTTPException을 임포트

async def ask_question(question: str):
    try:
        print("챗봇 응답을 준비 중...")  # 시작 로그

        # ollama.chat은 동기적으로 호출되므로 asyncio.to_thread로 비동기화
        response = await asyncio.to_thread(
            ollama.chat,
            model='gemma2',
            messages=[
                {"role": "system", "content": "당신은 유용한 한국어 챗봇입니다."},
                {"role": "user", "content": question}
            ]
        )

        print("응답을 받았습니다...")  # 응답 수신 후 로그

        if "message" not in response:
            raise HTTPException(status_code=500, detail="Ollama 응답 오류")
        
        print("응답 처리 중...")  # 응답 처리 중 로그
        return {"reply": response["message"]}

    except Exception as e:
        print(f"오류 발생: {str(e)}")  # 오류 발생 시 로그
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")