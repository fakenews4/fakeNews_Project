package com.example.FakeNews.controller;

import com.example.FakeNews.model.News;
import com.example.FakeNews.service.NewsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
public class NewsController {

    @Autowired
    private NewsService newsService;

    @GetMapping("/index")
    public String getNews(Model model) {
        List<News> newsList = newsService.getAllNews();
        model.addAttribute("newsList", newsList);
        return "news"; // news.jsp로 연결
    }
}
