package com.example.fakenews.controller;

import com.example.fakenews.service.VerificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class VerificationController {

    @Autowired
    private VerificationService verificationService;

    @PostMapping("/distinguish")
    public String verifyNews(@RequestParam String url, Model model) {
        // ✅ FastAPI에서 모든 기능 처리 후 결과 반환
        var verificationResult = verificationService.processVerification(url);

        System.out.println("반환데이터 = "+verificationResult);

        // ✅ JSP로 데이터 전달
        model.addAttribute("result", verificationResult);
        return "distinguish";  // ✅ `resultPage.jsp`로 이동
    }
}
