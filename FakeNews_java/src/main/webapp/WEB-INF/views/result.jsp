<%@ page import="java.io.*, java.net.*" %>
<%
    String title = request.getParameter("title");
    String content = request.getParameter("content");

    String urlStr = "http://localhost:8080/api/news/predict?title=" + URLEncoder.encode(title, "UTF-8") +
                    "&content=" + URLEncoder.encode(content, "UTF-8");

    URL url = new URL(urlStr);
    BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
    String prediction = reader.readLine();
    reader.close();
%>

<h2>결과:</h2>
<p>뉴스 제목: <%= title %></p>
<p>결과: <b><%= prediction %></b></p>