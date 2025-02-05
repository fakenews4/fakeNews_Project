<%@ page import="java.io.BufferedReader, java.io.InputStreamReader, java.net.HttpURLConnection, java.net.URL, org.json.JSONArray, org.json.JSONObject" %>
<%@ page contentType="text/html; charset=UTF-8" %>
<%
    response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    response.setHeader("Pragma", "no-cache");
    response.setDateHeader("Expires", 0);
%>
<%
    String query = "AI"; // 검색할 키워드
    int count = 5; // 가져올 뉴스 개수
    String apiUrl = "http://localhost:8000/fetch_news?query=" + query + "&count=" + count;

    try {
        URL url = new URL(apiUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "application/json");

        // 응답 데이터 읽기
        BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream()), "UTF-8"));
        StringBuilder responseBuilder = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            responseBuilder.append(line);
        }
        br.close();
        conn.disconnect();

        // JSON 파싱
        JSONObject jsonResponse = new JSONObject(responseBuilder.toString());
        if (jsonResponse.getString("status").equals("success")) {
            JSONArray newsArray = jsonResponse.getJSONArray("news");
%>
        <h2>뉴스 목록</h2>
        <ul>
        <%
            for (int i = 0; i < newsArray.length(); i++) {
                JSONObject newsItem = newsArray.getJSONObject(i);
        %>
            <li>
                <a href="<%= newsItem.getString("link") %>" target="_blank">
                    <strong><%= newsItem.getString("title") %></strong>
                </a>
                <p><%= newsItem.getString("description") %></p>
            </li>
        <%
            }
        %>
        </ul>
<%
        } else {
%>
        <p>뉴스 데이터를 가져오는 데 실패했습니다: <%= jsonResponse.getString("message") %></p>
<%
        }
    } catch (Exception e) {
%>
        <p>오류 발생: <%= e.getMessage() %></p>
<%
    }
%>
