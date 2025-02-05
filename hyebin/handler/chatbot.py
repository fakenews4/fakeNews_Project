import asyncio
import ollama
from fastapi import HTTPException

async def ask_question(question: str):
    try:
        response = await asyncio.to_thread(
            ollama.chat,
            model='gemma2',
            messages=[
                {"role": "system", "content": "당신은 유용한 한국어 챗봇입니다."},
                {"role": "user", "content": question}
            ]
        )

        if "message" not in response:
            raise HTTPException(status_code=500, detail="Ollama 응답 오류")

        return {"reply": response["message"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")
