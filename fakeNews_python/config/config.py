import os
from dotenv import load_dotenv
import pymysql

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 설정 함수
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),  # 기본값 3306
        charset="utf8mb4"
    )
