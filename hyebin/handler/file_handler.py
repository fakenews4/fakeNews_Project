from fastapi import UploadFile, HTTPException

async def upload_file(news_file: UploadFile):
    """텍스트 파일을 업로드하고 내용을 반환"""
    if not news_file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="지원되지 않는 파일 형식입니다. .txt 파일만 업로드하세요.")

    content = await news_file.read()
    text_content = content.decode("utf-8").strip()

    if not text_content:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")

    return {"success": True, "content": text_content}
