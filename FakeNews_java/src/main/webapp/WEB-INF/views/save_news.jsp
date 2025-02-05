<%@ page import="java.io.OutputStream, java.net.HttpURLConnection, java.net.URL" %>
<% // FastAPI의 /save_news 엔드포인트를 호출하여 MariaDB에 뉴스 저장
    String query = request.getParameter("query");
    String count = request.getParameter("count");
    String apiUrl = "http://localhost:8000/save_news?query=" + query + "&count=" + count;

    try {
        URL url = new URL(apiUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        // FastAPI 호출
        OutputStream os = conn.getOutputStream();
        os.flush();
        os.close();

        if (conn.getResponseCode() == 200) {
%>
        <p>뉴스 데이터가 성공적으로 저장되었습니다.</p>
<%
        } else {
%>
        <p>뉴스 저장에 실패했습니다.</p>
<%
        }
        conn.disconnect();
    } catch (Exception e) {
%>
        <p>오류 발생: <%= e.getMessage() %></p>
<%
    }
%>
