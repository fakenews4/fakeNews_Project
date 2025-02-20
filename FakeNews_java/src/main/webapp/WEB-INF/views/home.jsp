<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>메인 페이지</title>
</head>
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/main.css">
<script src="${pageContext.request.contextPath}/js/main.js"></script>
<body>
<div>
    <div id="main_header">
        <div id="main_logo">logo</div>
        <div id="main_recommend" onclick="move()">뉴스 추천</div>
    </div>
    <form action="/distinguish" method="POST">
        <label for="url">검증할 URL:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">검증하기</button>
    </form>

</div>
</body>
</html>
