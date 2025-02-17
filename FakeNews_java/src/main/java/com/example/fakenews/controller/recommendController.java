package com.example.fakenews.controller;

import com.example.fakenews.dto.recommendDTO;
import com.example.fakenews.service.recommendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
public class recommendController {

    @Autowired
    private recommendService recommendservice;

    @GetMapping("/recommend")
    public String showRecommendPage(@RequestParam("keywords") String keywords, Model model) {
        System.out.println("📌 JSP 렌더링 시작 - keywords: " + keywords);

        // FastAPI에서 뉴스 데이터 가져오기
        List<recommendDTO> articles = recommendservice.fetchRecommendedArticles(keywords);
        model.addAttribute("articles", articles);

        System.out.println("📌 JSP에서 사용할 뉴스 개수: " + articles.size());

        return "recommend";
    }

    @PostMapping("/api/recommend")
    @CrossOrigin(origins = "http://localhost:8000")  // ✅ POST 요청에 직접 CORS 허용 추가
    @ResponseBody
    public ResponseEntity<Map<String, Object>> receiveFastAPIData(@RequestBody Map<String, Object> requestData) {
        System.out.println("📌 받은 데이터: " + requestData);

        // "keywords" 값 확인
        String keywords = (String) requestData.getOrDefault("keywords", "korea");

        // FastAPI에서 추천 뉴스 가져오기
        List<recommendDTO> articles = recommendservice.fetchRecommendedArticles(keywords);

        // JSON으로 응답 반환
        Map<String, Object> response = new HashMap<>();
        response.put("articles", articles);

        return ResponseEntity.ok(response);
    }
}
