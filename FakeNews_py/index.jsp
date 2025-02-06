<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="result.jsp" method="post">
        <label>뉴스 제목:</label>
        <input type="text" name="title" required>
        <br>
        <label>뉴스 본문:</label>
        <textarea name="content" required></textarea>
        <br>
        <button type="submit">뉴스 분석</button>
    </form>
</body>
</html>