<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<html>
<head>
    <title>title</title>
</head>
<body>
<ul>
    <c:forEach var="article" items="${articles}">
        <li>
            <h3><a href="${article.link}">${article.title}</a></h3>
            <p>${article.description}</p>
        </li>
    </c:forEach>
</ul>
</body>
</html>
