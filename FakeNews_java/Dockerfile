# 1️⃣ Tomcat을 기반으로 컨테이너 생성
FROM tomcat:9.0-jdk17-temurin

# 2️⃣ 빌드된 WAR 파일을 Tomcat의 webapps 디렉토리에 복사
COPY build/libs/fakenews-0.0.1-SNAPSHOT.war /usr/local/tomcat/webapps/fakenews.war

# 3️⃣ Tomcat 실행
EXPOSE 8080
CMD ["catalina.sh", "run"]
