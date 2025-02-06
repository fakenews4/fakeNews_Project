from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from fastapi import HTTPException

async def crawl_url(url: str):
    try:
        options = Options()
        options.headless = True
        options.add_argument("--ignore-certificate-errors")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)

        try:
            content = driver.find_element(By.TAG_NAME, 'article').text
        except Exception:
            content = ""

        driver.quit()

        if content:
            return {"extracted_content": content}
        else:
            raise HTTPException(status_code=500, detail="웹 페이지에서 콘텐츠를 추출할 수 없습니다.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"크롤링 중 오류 발생: {str(e)}")
