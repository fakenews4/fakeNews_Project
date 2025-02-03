package com.fakenews.compose.service;

import com.fakenews.compose.dto.recommendDTO;
import org.jsoup.Jsoup;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.List;

@Service
public class recommendService {

    private static final String FASTAPI_URL = "http://localhost:8000/news/recommend?keywords=";

    public List<recommendDTO> fetchRecommendedArticles(String keywords) {
        RestTemplate restTemplate = new RestTemplate();
        List<recommendDTO> articles = new ArrayList<>();

        try {
            // FastAPI에서 JSON 데이터 가져오기
            String response = restTemplate.getForObject(FASTAPI_URL + keywords, String.class);
            System.out.println("📌 FastAPI 응답: " + response);

            JSONArray articlesArray;
            if (response.startsWith("{")) { // JSON이 객체인지 배열인지 확인
                JSONObject jsonResponse = new JSONObject(response);
                System.out.println("오브젝트");
                if (!jsonResponse.has("news")) {
                    throw new RuntimeException("📌 FastAPI 응답에 'news' 키가 없음");
                }
                articlesArray = jsonResponse.getJSONArray("news");
            } else {
                articlesArray = new JSONArray(response);
                System.out.println("리스트");
            }

            System.out.println("📌 articlesArray 크기: " + articlesArray.length());

            // JSON 데이터를 DTO 리스트로 변환
            for (int i = 0; i < articlesArray.length(); i++) {
                JSONObject obj = articlesArray.getJSONObject(i);

                System.out.println(obj.toString());

                recommendDTO dto = new recommendDTO(
                        obj.optString("title", "No Title"),
                        obj.optString("link", "No Link"),
                        Jsoup.parse(obj.optString("description", "No Description")).text() // HTML 태그 제거
                );

                System.out.println("📌 변환된 DTO: " + dto.toString());
                articles.add(dto);
            }

            System.out.println("📌 최종 DTO 리스트: " + articles);
            return articles;
        } catch (Exception e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }
}
