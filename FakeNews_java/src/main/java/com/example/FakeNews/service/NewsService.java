package com.example.FakeNews.service;

import com.example.FakeNews.model.News;
import org.springframework.stereotype.Service;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

@Service
public class NewsService {

    public String predictNews(String title, String content) {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("python3", "models/predict.py", title, content);
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            List<String> output = new ArrayList<>();
            while ((line = reader.readLine()) != null) {
                output.add(line);
            }
            process.waitFor();
            return output.get(0); // Python 스크립트의 첫 번째 출력값 (예측 결과)
        } catch (Exception e) {
            e.printStackTrace();
            return "Error";
        }
    }

    public void saveAnnotation(String title, String content, String label) {
        // 여기에 데이터베이스 저장 로직 구현
        System.out.println("Saved annotation: " + title + " | " + label);
    }

    public List<News> getAllNews() {
        // 뉴스 데이터 생성(DB에서 가져옴)
        List<News> newsList = new ArrayList<>();
        newsList.add(new News(1L, "제목 1", "내용 1", LocalDate.now()));
        newsList.add(new News(2L, "제목 2", "내용 2", LocalDate.now().minusDays(1)));
        newsList.add(new News(3L, "제목 3", "내용 3", LocalDate.now().minusDays(2)));
        return newsList;
    }
}
