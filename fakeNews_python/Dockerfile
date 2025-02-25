# Python 3.10.6 slim 기반 이미지
FROM python:3.10.6-slim

# 작업 디렉토리 설정
WORKDIR /app

# 기본 패키지 설치 (Java 17, C++ 컴파일러 포함)
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    curl \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Java 환경변수 설정 (Konlpy에서 사용됨)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# ✅ GPU 관련 경고 방지 (CPU 전용 실행)
ENV CUDA_VISIBLE_DEVICES=""
ENV TF_CPP_MIN_LOG_LEVEL=3

# gRPC 오류 억제
ENV GRPC_VERBOSITY=ERROR
ENV GRPC_TRACE=""

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
