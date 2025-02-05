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
    
    
# 도메인과 언론사 이름 매핑
PUBLISHER_MAPPING = {
    # 전국종합일간지
    "khan.co.kr": "경향신문",
    "kmib.co.kr": "국민일보",
    "naeil.com": "내일신문",
    "donga.com": "동아일보",
    "munhwa.com": "문화일보",
    "seoul.co.kr": "서울신문",
    "segye.com": "세계일보",
    "asiatoday.co.kr": "아시아투데이",
    "chosun.com": "조선일보",
    "joins.com": "중앙일보",
    "hani.co.kr": "한겨레",
    "hankookilbo.com": "한국일보",

    # 지역종합일간지
    "kado.net": "강원도민일보",
    "kwnews.co.kr": "강원일보",
    "kgnews.co.kr": "경기신문",
    "kyeonggi.com": "경기일보",
    "idomin.com": "경남도민일보",
    "knnews.co.kr": "경남신문",
    "gnnews.co.kr": "경남일보",
    "hidomin.com": "경북도민일보",
    "kbmaeil.com": "경북매일신문",
    "kyongbuk.co.kr": "경북일보",
    "ksilbo.co.kr": "경상일보",
    "kyeongin.com": "경인일보",
    "gnnews.co.kr": "광남일보",
    "kjdaily.com": "광주매일신문",
    "kwangju.co.kr": "광주일보",
    "kookje.co.kr": "국제신문",
    "ggilbo.com": "금강일보",
    "kihoilbo.co.kr": "기호일보",
    "namdonews.com": "남도일보",
    "idaegu.co.kr": "대구신문",
    "idaegu.com": "대구일보",
    "daejonilbo.com": "대전일보",
    "dynews.co.kr": "동양일보",
    "imaeil.com": "매일신문",
    "moodeungilbo.co.kr": "무등일보",
    "busan.com": "부산일보",
    "sjbnews.com": "새전북신문",
    "yeongnam.com": "영남일보",
    "iusm.co.kr": "울산매일",
    "ulsanpress.net": "울산신문",
    "incheonilbo.com": "인천일보",
    "jnilbo.com": "전남일보",
    "jeonra.com": "전라일보",
    "jjan.kr": "전북도민일보",
    "jbyonhap.com": "전북일보",
    "jemin.com": "제민일보",
    "jejunews.com": "제주일보",
    "joongdo.co.kr": "중도일보",
    "jbnews.com": "중부매일",
    "joongboo.com": "중부일보",
    "cbinews.co.kr": "충북일보",
    "ccdailynews.com": "충청일보",
    "cctimes.kr": "충청타임즈",
    "cctoday.co.kr": "충청투데이",
    "hallailbo.co.kr": "한라일보",

    # 경제일간지
    "dnews.co.kr": "대한경제",
    "mk.co.kr": "매일경제",
    "mt.co.kr": "머니투데이",
    "metroseoul.co.kr": "메트로경제",
    "viva100.com": "브릿지경제",
    "sedaily.com": "서울경제",
    "asiae.co.kr": "아시아경제",
    "ajunews.com": "아주경제",
    "ekn.kr": "에너지경제",
    "edaily.co.kr": "이데일리",
    "etoday.co.kr": "이투데이",
    "fnnews.com": "파이낸셜뉴스",
    "hankyung.com": "한국경제",
    "heraldcorp.com": "헤럴드경제",

    # 스포츠일간지
    "sports.khan.co.kr": "스포츠경향",
    "sports.donga.com": "스포츠동아",
    "sportsseoul.com": "스포츠서울",
    "sportsworldi.com": "스포츠월드",
    "sports.hankooki.com": "스포츠한국",
    "isplus.live.joins.com": "일간스포츠",

    # 영자일간지
    "koreajoongangdaily.joins.com": "코리아중앙데일리",
    "koreatimes.co.kr": "코리아타임스",
    "koreaherald.com": "코리아헤럴드",

    # 전문일간지 및 어린이신문
    "nongmin.com": "농민신문",
    "dt.co.kr": "디지털타임스",
    "kids.hankooki.com": "소년한국일보",
    "kids.kado.net": "어린이강원일보",
    "kids.donga.com": "어린이동아",
    "etnews.com": "전자신문",
    "hkbs.co.kr": "환경일보",

    # 종합·전문주간지
    "journalist.or.kr": "기자협회보",
    "mediatoday.co.kr": "미디어오늘",
    "sisain.co.kr": "시사IN",
    "economist.co.kr": "이코노미스트",
    "ilyo.co.kr": "일요신문",
    "weekly.hankooki.com": "주간한국",
    "sunday.joins.com": "중앙선데이",
    "h21.hani.co.kr": "한겨레21",

    # 지역주간지
    "gyotongn.com": "고양신문",
    "gynet.co.kr": "광양신문",
    "gimpo.com": "김포신문",
    "newsseocheon.com": "뉴스서천",
    "djtimes.co.kr": "당진시대",
    "wooriy.com": "영암우리신문",
    "yeongjuilbo.com": "영주시민신문",
    "okinews.com": "옥천신문",
    "wjtoday.com": "원주투데이",
    "soraknews.co.kr": "주간설악신문",
    "pttimes.com": "평택시민신문",
    "hsnews.co.kr": "홍성신문",
}
 

