import asyncio
import ollama
from fastapi import HTTPException

async def summarize_content(content: str):
    try:
        summarize_question = f"다음 내용을 요약해 주세요: {content}"
        response = await asyncio.to_thread(
            ollama.chat,
            model='gemma2',
            messages=[
                {"role": "system", "content": "당신은 유용한 한국어 챗봇입니다."},
                {"role": "user", "content": summarize_question}
            ]
        )

        if "message" not in response:
            raise HTTPException(status_code=500, detail="Ollama 응답 오류")
        
        return {"summary": response["message"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류 발생: {str(e)}")
