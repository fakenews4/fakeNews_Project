# 데이터베이스 연결
import pymysql
import pymysql.cursors

# MariaDB 연결 설정
DB_CONFIG = {
    "host": "localhost",      # 데이터베이스 주소
    "user": "root",           # 사용자 이름
    "password": "1234",       # 비밀번호
    "database": "sys",        # 사용할 데이터베이스 이름
    "charset": "utf8mb4"
}

# 데이터베이스 테이블 생성
def create_table():
    """
    news 테이블 생성 함수
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL UNIQUE,
            content TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
    finally:
        conn.close()

# 데이터 저장(중복 확인 포함)
def save_news_to_db(title, content):
    """
    뉴스 데이터를 MariaDB에 저장하는 함수(중복 데이터는 저장하지 않음)
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        # 중복 확인
        insert_query = "INSERT INTO(*) FROM news WHERE title = %s)"
        cursor.execute(insert_query, (title, ))
        if cursor.fetchone()[0] == 0:
            # 중복되지 않은 경우에만 저장
            insert_query = "INSERT INTO news (title, content) VALUES (%s %s)"
            cursor.execute(insert_query, (title, content))
            conn.commit()
            print(f"'{title}' 저장 완료")
        else:
            print(f"'{title}' 중복으로 저장되지 않음")
    finally:
        conn.close()
    
# 데이터 불러오기
def fetch_all_news():
    """
    데이터베이스에서 모든 뉴스 데이터를 가져오는 함수
    :return: [{"id": 1, "title": "제목1", "content": "내용1", "date": "2023-01-01"}, ...]
    """
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        select_query = "SELECT * FROM news"
        cursor.execute(select_query)
        return cursor.fetchall()
    finally:
        conn.close()

if __name__ == "__main__":
    create_table()
    print("news 테이블이 생성되었거나 이미 존재합니다.")