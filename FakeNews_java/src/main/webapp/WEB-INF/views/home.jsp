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
            flex-direction: column;
            position: relative;
        }

        /* 오른쪽 상단 뉴스 추천 버튼 */
        #main_recommend {
            position: absolute;
            top: 20px;
            right: 30px;
            background: #007bff;
            color: white;
            padding: 10px 15px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
            width: 120px;
            text-align: center;
        }

        #main_recommend:hover {
            background: #0056b3;
        }

        /* 로고 */
        #main_logo img {
            width: 180px;
            height: auto;
            margin-bottom: 20px;
        }

        /* 검색 입력창 스타일 */
        input[type="text"] {
            width: 500px;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 30px;
            font-size: 14px; /* 기존 18px → 14px */
            text-align: center;
            outline: none;
            background-color: rgba(255, 255, 255, 0.8);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        /* 검색 버튼 */
        button {
            width: 180px; /* 기존 200px → 180px */
            padding: 12px; /* 기존 15px → 12px */
            background: #28a745;
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-size: 14px; /* 기존 16px → 14px */
            transition: background 0.3s;
            margin-top: 10px;
        }

        button:hover {
            background: #218838;
        }

    </style>
</head>
<body>

    <!-- 뉴스 추천 버튼 -->
    <div id="main_recommend" onclick="move()">뉴스 추천</div>

    <!-- 로고 -->
    <div id="main_logo">
        <img src="${pageContext.request.contextPath}/images/logo.png" alt="logo">
    </div>

    <!-- 검색 입력창과 버튼 -->
    <form action="/distinguish" method="POST">
        <input type="text" id="url" name="url" placeholder="검증할 URL을 입력하세요" required>
        <button type="submit">검증하기</button>
    </form>

</body>
</html>
