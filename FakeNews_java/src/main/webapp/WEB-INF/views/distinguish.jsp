<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<head>
    <title>뉴스 판별</title>
</head>
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/distinguish.css">
<script src="${pageContext.request.contextPath}/js/distinguish.js"></script>
<body>
<div>
    <div id="main_box">
        <h3>뉴스 판별 페이지</h3>
        <p>${result.summary}</p>
        <p>${result.analysis.label}</p>
        <p>${result.analysis.credibility_score}</p>
        <p>${result.analysis.gemini_analysis}</p>
    </div>
</div>
</body>
</html>
