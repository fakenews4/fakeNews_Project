<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>메인 페이지</title>
</head>
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/main.css">
<script src="${pageContext.request.contextPath}/js/main.js"></script>
<body>
<div>
    <div onclick="move()">뉴스 추천</div>
    <div id="main_box">
        <h3>뉴스 판별 사이트</h3>
        <input type="text" placeholder="링크를 입력해주세요.">
        <div id="discrimination" onclick="dis()">뉴스 판별</div>
    </div>
</div>
</body>
</html>
