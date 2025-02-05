package com.example.FakeNews.model;

import java.time.LocalDate;

public class News {
    private Long id; // 뉴스 ID
    private String title; // 뉴스 제목
    private String content; // 뉴스 내용
    private LocalDate date; // 작성 날짜

    // 생성자
    public News() {}

    public News(Long id, String title, String content, LocalDate date) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.date = date;
    }

    // Getter와 Setter
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }
}