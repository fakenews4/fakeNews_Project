package com.fakenews.compose.controller;

import com.fakenews.compose.dto.recommendDTO;
import com.fakenews.compose.service.recommendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class recommendController {

    @Autowired
    private recommendService recommendservice;

    @GetMapping("/recommend")
    public String showRecommendedArticles(@RequestParam("keywords") String keywords, Model model) {
        List<recommendDTO> articles = recommendservice.fetchRecommendedArticles(keywords);
        model.addAttribute("articles", articles);
        return "recommend";
    }
}
 