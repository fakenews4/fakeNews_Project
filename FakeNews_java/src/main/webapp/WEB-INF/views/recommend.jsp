<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<head>
    <title>뉴스 기사</title>
    <!-- Bootstrap CDN 추가 -->
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>

<div class="container mt-4">
    <h2 class="text-center mb-4">📰 추천 뉴스</h2>
    <button onclick="history.back()" class="btn btn-secondary mb-4">⬅ 이전 페이지</button>


    <div class="row">
        <c:forEach var="article" items="${articles}">
            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm">

                    <div class="card-body">
                        <h5 class="card-title">
                            <a href="${article.link}" target="_blank" class="text-dark text-decoration-none">
                                    ${article.title}
                            </a>
                        </h5>
                        <p class="card-text">${article.description}</p>
                    </div>

                    <div class="card-footer text-muted">
                        🏢 ${article.publisher}
                    </div>
                </div>
            </div>
        </c:forEach>
    </div>
</div>

<!-- Bootstrap JS 추가 -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
