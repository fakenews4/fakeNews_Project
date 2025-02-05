package com.fakenews.compose.controller;

import com.fakenews.compose.service.newsService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/news")
public class newsController {

    private final newsService newsService;

    public newsController(newsService newsService) {
        this.newsService = newsService;
    }

    @GetMapping
    public String getNews(@RequestParam(required = false) String query, Model model) {
        String newsData = newsService.fetchNews(query);
        model.addAttribute("news", newsData);
        return "news";
    }
}
