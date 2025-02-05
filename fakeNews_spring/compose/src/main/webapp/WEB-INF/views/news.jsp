<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>뉴스 분석</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/static/css/main.css">
    <script src="${pageContext.request.contextPath}/static/js/chatbot.js"></script>
</head>
<body>
<h1>뉴스 분석 페이지</h1>
<p>검색어를 입력하세요.</p>
<form action="${pageContext.request.contextPath}/news" method="get">
    <input type="text" name="query">
    <button type="submit">검색</button>
</form>

<c:if test="${not empty news}">
    <h2>검색 결과:</h2>
    <pre>${news}</pre>
</c:if>

<script>
    function fetchNews() {
        let query = document.getElementById("query").value;
        fetch("${pageContext.request.contextPath}/api/news?query=" + query)
            .then(response => response.json())
            .then(data => {
                document.getElementById("news-result").innerHTML = JSON.stringify(data);
            });
    }
</script>

<div id="news-result"></div>
</body>
</html>
