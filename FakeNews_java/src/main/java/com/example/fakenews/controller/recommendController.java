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
    public String showRecommendPage(@RequestParam(value = "keywords", defaultValue = "korea") String keywords, Model model) {
        System.out.println("📌 JSP 렌더링 시작 - 원본 keywords: " + keywords);

        // ✅ URL 인코딩 문제 해결 (디코딩 수행)
        String decodedKeywords = java.net.URLDecoder.decode(keywords, java.nio.charset.StandardCharsets.UTF_8);

        // ✅ 대괄호 제거 (["삼성"] → 삼성)
        decodedKeywords = decodedKeywords.replaceAll("[\\[\\]\"]", "");
        System.out.println("📌 정리된 keywords: " + decodedKeywords);

        // ✅ FastAPI에서 뉴스 데이터 가져오기
        List<recommendDTO> articles = recommendservice.fetchRecommendedArticles(decodedKeywords);
        model.addAttribute("articles", articles);

        System.out.println("📌 JSP에서 사용할 뉴스 개수: " + articles.size());

        return "recommend";
    }
}
