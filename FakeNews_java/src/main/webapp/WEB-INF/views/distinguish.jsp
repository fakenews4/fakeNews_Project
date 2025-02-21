<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<head>
    <title>뉴스 판별</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/distinguish.css">
    <script src="${pageContext.request.contextPath}/js/distinguish.js"></script>
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white text-center">
                    <h3>뉴스 판별 결과</h3>
                </div>
                <div class="card-body">
                    <p class="fw-bold">요약:</p>
                    <p>${result.summary}</p>
                    <hr>
                    <p class="fw-bold">분석 결과:</p>
                    <p class="text-muted">${result.analysis.label}</p>
                    <hr>
                    <p class="fw-bold">신뢰도 점수:</p>
                    <p class="text-success fw-semibold">${result.analysis.credibility_score}</p>
                    <hr>
                    <p class="fw-bold">Gemini AI 분석:</p>
                    <p class="text-info">${result.analysis.gemini_analysis}</p>
                </div>
            </div>
        </div>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
