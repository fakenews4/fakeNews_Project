package com.example.fakenews.service;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import java.util.Map;

@Service
public class VerificationService {

    @Autowired
    private WebClient.Builder webClientBuilder;  // ✅ FastAPI에 요청할 WebClient

    private static final String FASTAPI_API = "http://localhost:8000/api/crawler?url=";  // ✅ FastAPI에서 모든 기능 처리

    public Map<String, Object> processVerification(String url) {
        String response = webClientBuilder.build()
                .get()
                .uri(FASTAPI_API + url)
                .retrieve()
                .bodyToMono(String.class)
                .block();  // ✅ 동기 방식

        // ✅ JSON을 Map으로 변환
        return new JSONObject(response).toMap();
    }
}
