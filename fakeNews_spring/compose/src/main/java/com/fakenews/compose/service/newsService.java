package com.fakenews.compose.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class newsService {

    public String fetchNews(String query) {
        if (query == null || query.isEmpty()) {
            return "검색어를 입력하세요.";
        }

        String fastApiUrl = "http://localhost:8000/news?query=" + query;
        RestTemplate restTemplate = new RestTemplate();
        return restTemplate.getForObject(fastApiUrl, String.class);
    }
}
