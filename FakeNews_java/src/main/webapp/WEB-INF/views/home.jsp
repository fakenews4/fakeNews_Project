<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>메인 페이지</title>
    <link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/css/main.css">
    <script src="${pageContext.request.contextPath}/js/main.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        #main_container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 350px;
        }
        #main_header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            font-weight: bold;
        }
        #main_logo {
            font-size: 24px;
            color: #333;
        }
        #main_recommend {
            cursor: pointer;
            background: #007bff;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        #main_recommend:hover {
            background: #0056b3;
        }
        form {
            margin-top: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            margin-top: 10px;
            width: 100%;
            padding: 10px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        button:hover {
            background: #218838;
        }
    </style>
</head>
<body>
<div id="main_container">
    <div id="main_header">
        <div id="main_logo">Logo</div>
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
