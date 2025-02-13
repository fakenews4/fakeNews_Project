package com.fakenews.compose.controller;

import com.fakenews.compose.dto.recommendDTO;
import com.fakenews.compose.service.recommendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

@RestController  // ✅ JSON 응답을 반환하는 API 컨트롤러
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:8000")  // ✅ CORS 허용
public class ApiRecommendController {

    @Autowired
    private recommendService recommendservice;

    // ✅ FastAPI 데이터를 POST 요청으로 받고 JSON 응답 반환
    @PostMapping("/recommend")
    public ResponseEntity<Map<String, Object>> receiveFastAPIData(@RequestBody Map<String, Object> requestData) {
        System.out.println("📌 받은 데이터: " + requestData);

        // "keywords" 값이 있는지 확인하고 가져오기
        String keywords = (String) requestData.getOrDefault("keywords", "korea");

        // FastAPI에서 추천 뉴스 가져오기
        List<recommendDTO> articles = recommendservice.fetchRecommendedArticles(keywords);

        // JSON으로 응답 반환
        Map<String, Object> response = new HashMap<>();
        response.put("articles", articles);

        return ResponseEntity.ok(response);
    }
}
