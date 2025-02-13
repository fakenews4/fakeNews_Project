package com.fakenews.compose.controller;

import com.fakenews.compose.dto.recommendDTO;
import com.fakenews.compose.service.recommendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller  // ✅ JSP 렌더링 전용 컨트롤러
public class recommendController {

    @Autowired
    private recommendService recommendservice;

    // ✅ GET 요청으로 JSP 페이지 렌더링
    @GetMapping("/recommend")
    public String showRecommendedArticles(
            @RequestParam(value = "keywords", defaultValue = "korea") String keywords,
            Model model) {

        // FastAPI에서 추천 뉴스 가져오기
        List<recommendDTO> articles = recommendservice.fetchRecommendedArticles(keywords);

        // JSP로 데이터 전달
        model.addAttribute("articles", articles);

        System.out.println("📌 JSP로 데이터 전달 완료");
        return "recommend";  // `recommend.jsp`로 이동
    }
}
