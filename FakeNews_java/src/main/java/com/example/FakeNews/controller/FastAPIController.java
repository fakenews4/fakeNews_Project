package com.example.FakeNews.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.util.Map;


@Controller
public class FastAPIController {

    private final RestTemplate restTemplate = new RestTemplate();

    @GetMapping("/fastapi-data")
    public String getFastAPIData(Model model) {
        // 1. RestTemplate 사용하여 http://localhost:8000/fastapi/data에 요청 보냄
        String url = "http://localhost:8000/fastapi/data";  // ✅ FastAPI 엔드포인트

        try {
            ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);
            
            // 2. 응답 데이터 Model에 저장하여 JSP에 사용할 수 있도록 설정
            model.addAttribute("fastApiData", response.getBody()); // JSP에 데이터 전달
        } catch (Exception e) { // 3. 예외 발생 시 "FastAPI 요청 실패"라는 메시지를 JSP에 표시
            model.addAttribute("fastApiData", Map.of("message", "FastAPI 요청 실패", "status", "500"));
        }

        return "fastapi";  // fastapi.jsp로 이동
    }
}

