<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>

<c:set var="keywordsJson" value="${fn:replace(result.keywords, ' ', '')}" />
<html>
<head>
    <title>뉴스 판별</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <button onclick="window.location.href='http://localhost:8080/'" class="btn btn-secondary"
                    style="width: 150px; white-space: normal;">⬅ 이전 페이지</button>
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white text-center">
                    <h3>뉴스 판별 결과</h3>
                </div>
                <div class="card-body">
                    <p class="fw-bold">요약:</p>
                    <pre style="white-space: normal;">${result.summary}</pre>
                    <hr>
                    <pre class="fw-bold">분석 결과:</pre>
                    <pre class="text-muted">${result.analysis.label}</pre>
                    <hr>
                    <pre class="fw-bold">신뢰도 점수:</pre>
                    <pre class="text-success fw-semibold">${result.analysis.credibility_score}</pre>
                    <hr>
                    <pre class="fw-bold">Gemini AI 분석:</pre>
                    <pre class="text-info" style="color:black;">${fn:replace(result.analysis.gemini_analysis,"*","")}</pre>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    document.addEventListener("DOMContentLoaded", function () {
        try {
            // ✅ JSP에서 JSON 데이터를 안전하게 가져오기
            var keywords = '<c:out value="${keywordsJson}" />';

            console.log("✅ JSP에서 가져온 원본 키워드:", keywords);

            // ✅ 만약 JSON 형식이 아니라면 강제 변환
            if (!keywords.startsWith("[") || !keywords.endsWith("]")) {
                console.warn("⚠️ 키워드가 JSON 형식이 아님. 변환 시도...");
                keywords = '["' + keywords.replace(/,\s*/g, '", "') + '"]';
            }

            // ✅ JSON 변환
            var keywordArray = JSON.parse(keywords);
            console.log("✅ JSON 변환 성공:", keywordArray);

            // ✅ 기존 데이터 삭제 후 localStorage에 저장
            localStorage.removeItem("keywords");

            if (Array.isArray(keywordArray) && keywordArray.length > 0) {
                localStorage.setItem("keywords", JSON.stringify(keywordArray));
                console.log("✅ 저장된 키워드:", keywordArray);
            } else {
                console.log("⚠️ 키워드 없음");
            }
        } catch (error) {
            console.error("❌ JSON 변환 오류:", error);
            console.error("❌ 변환 실패한 데이터:", keywords);
        }
    });

</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
