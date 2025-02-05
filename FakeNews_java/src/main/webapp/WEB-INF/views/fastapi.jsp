<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI 데이터</title>
</head>
<body>
    <h2>FastAPI에서 받은 데이터</h2>
    <p>메시지: ${fastApiData.message}</p>
    <p>상태: ${fastApiData.status}</p>

    <c:if test="${fastApiData.status == '500'}">
        <p style="color: red;">⚠️ FastAPI 응답 실패! 서버 상태를 확인하세요.</p>
    </c:if>
</body>
</html>

<%-- 1. ${fastApiData.message} 와 ${fastApiData.status}로 FastAPI 데이터 표시 --%>
<%-- 2. FastAPI 요청 실패하면 "FastAPI 응답 실패" 경고 메시지 보여 줌 --%>