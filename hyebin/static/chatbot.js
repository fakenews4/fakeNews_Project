const sendMessageButton = document.getElementById("send-message");
const userInput = document.getElementById("user-input");
const chatbotMessages = document.getElementById("chatbot-messages");

const crawlButton = document.getElementById("crawl-button");
const linkInput = document.getElementById("news-link");

let crawledContent = null;
let uploadedContent = null;
let crawledUrl = null;

const uploadButton = document.getElementById("upload-button");
const fileInput = document.getElementById("news-file");
const chatbox = document.getElementById("chatbox");

const predefinedResponses = {
    "안녕": "안녕하세요! 무엇을 도와드릴까요? 😊",
    "가짜 뉴스란?": "가짜 뉴스는 사실이 아닌 정보나 거짓된 뉴스를 의미합니다.",
};

function displayChatbotMessage(message, isUser = false) {
    const messageElement = document.createElement('p');
    messageElement.innerHTML = (isUser ? `<strong>사용자:</strong> ` : `<strong>챗봇:</strong> `) + message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    return messageElement;
}

async function crawlNews(url) {
    try {   
        const response = await fetch("http://127.0.0.1:8000/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });
        const result = await response.json();
        console.log("✅ 크롤링 결과:", result);

        const extractedContent = result.extracted_content || "웹 콘텐츠를 추출할 수 없습니다.";
        if (extractedContent === "웹 콘텐츠를 추출할 수 없습니다.") {
            alert("웹 콘텐츠를 추출할 수 없습니다.");
            return;
        }

        crawledContent = extractedContent;
        displayChatbotMessage("뉴스 링크가 업로드되었습니다.", false);
        crawledUrl = url;

        // 키워드 추출은 백엔드에서 처리하지만, 화면에는 표시하지 않음
        const keywordResponse = await fetch("http://127.0.0.1:8000/keywords", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });
        const keywordResult = await keywordResponse.json();
        console.log("✅ 추출된 키워드:", keywordResult);
        if (keywordResult.keywords && keywordResult.keywords.length > 0) {
            localStorage.setItem("keywords", JSON.stringify(keywordResult.keywords));
            console.log("✅ 키워드 로컬스토리지 저장 완료:", keywordResult.keywords);
        } else {
            console.error("키워드 추출 실패:", keywordResult);
        }

    } catch (error) {
        console.error("크롤링 오류:", error);
        displayChatbotMessage("크롤링 중 오류가 발생했습니다.");
    }
}

crawlButton.addEventListener("click", async () => {
    const url = linkInput.value;
    if (url.trim()) {
        crawlNews(url);
    } else {
        alert("URL을 입력해 주세요.");
    }
});

sendMessageButton.addEventListener("click", async () => {
    const userMessage = userInput.value;
    if (userMessage.trim()) {
        displayChatbotMessage(userMessage, true);
        const typingMessage = displayChatbotMessage("입력 중...");

        if (predefinedResponses[userMessage]) {
            typingMessage.innerHTML = `<strong>챗봇:</strong> ${predefinedResponses[userMessage]}`;
        } else if (crawledUrl && crawledContent && userMessage.includes("크롤링")) {
            typingMessage.innerHTML = `<strong>챗봇:</strong> 크롤링된 뉴스 콘텐츠: ${crawledContent}`;
            try {
                const response = await fetch("http://127.0.0.1:8000/summarize", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ content: crawledContent })
                });
                const result = await response.json();
                let summary = "";
                if (typeof result.summary === "object" && result.summary !== null) {
                    // 객체 내 내용을 가져오기 위해 접근
                    summary = result.summary.content || JSON.stringify(result.summary); // 예시: content 필드가 있을 경우 사용
                } else {
                    summary = result.summary;
                }
                typingMessage.innerHTML = `<strong>챗봇:</strong> ${summary}`;
            } catch (error) {
                console.error("요약 요청 오류:", error);
                typingMessage.innerHTML = `<strong>챗봇:</strong> 요약 생성 중 오류가 발생했습니다.`;
            }
        } else if (userMessage.startsWith("http://") || userMessage.startsWith("https://")) {
            crawlNews(userMessage);
        } else if (userMessage.includes("요약")) {
            // 요약 요청: 크롤링한 뉴스 또는 업로드한 파일 중 최신 데이터를 요약
            let contentToSummarize = crawledContent || uploadedContent;
        
            if (!contentToSummarize) {
                typingMessage.innerHTML = `<strong>챗봇:</strong> 요약할 내용이 없습니다. 먼저 크롤링하거나 파일을 업로드하세요.`;
                return;
            }
        
            try {
                const response = await fetch("http://127.0.0.1:8000/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ content: contentToSummarize })
                });
                const result = await response.json();
                let summary = result.summary || "요약을 생성할 수 없습니다.";
                
                // 만약 summary가 객체라면 내부의 내용을 확인
                if (typeof summary === "object") {
                    summary = summary.content || JSON.stringify(summary);
                }

                typingMessage.innerHTML = `<strong>챗봇:</strong> ${summary}`;
            } catch (error) {
                console.error("요약 요청 오류:", error);
                typingMessage.innerHTML = `<strong>챗봇:</strong> 요약 생성 중 오류가 발생했습니다.`;
            }
        } else {
            try {
                const response = await fetch("http://127.0.0.1:8000/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question: userMessage })
                });
                const result = await response.json();
                let replyText = "";
                if (typeof result.reply === "object" && result.reply !== null) {
                    replyText = result.reply.content;
                } else {
                    replyText = result.reply;
                }
                typingMessage.innerHTML = `<strong>챗봇:</strong> ${replyText}`;
            } catch (error) {
                console.error("질문 처리 오류:", error);
                typingMessage.innerHTML = `<strong>챗봇:</strong> 처리 중 오류가 발생했습니다.`;
            }
        }
        userInput.value = "";
    } else {
        alert("입력한 질문이 없습니다.");
    }
});


uploadButton.addEventListener("click", async () => {
    const file = fileInput.files[0];

    if (!file) {
        alert("업로드할 파일을 선택하세요.");
        return;
    }

    const formData = new FormData();
    formData.append("news_file", file);

    try {
        console.log("📤 [UPLOAD] 파일 업로드 요청 시작!");

        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        console.log("📥 [UPLOAD] 서버 응답 상태:", response.status);

        const result = await response.json();
        console.log("✅ [UPLOAD] 파일 업로드 결과:", result);

        if (result.success) {
            uploadedContent = result.content;  // 파일 내용을 저장
            displayChatbotMessage("파일이 업로드 되었습니다.", false);

            console.log("🔍 [KEYWORDS] 키워드 추출 요청 시작");
            
            const keywordsResponse = await fetch("http://127.0.0.1:8000/keywords_from_text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content: result.content })  // ✅ 'text' 대신 'result.content' 사용
            });

            console.log("📥 [KEYWORDS] 서버 응답 상태:", keywordsResponse.status);

            const keywordsResult = await keywordsResponse.json();
            console.log("✅ [KEYWORDS] 추출 결과:", keywordsResult);

            // ✅ 로컬 스토리지에 저장 추가
            if (keywordsResult.success) {
                localStorage.setItem("keywords", JSON.stringify(keywordsResult.keywords));
                console.log("✅ 키워드가 로컬 스토리지에 저장됨:", keywordsResult.keywords);
            } else {
                console.error("❌ 키워드 추출 실패:", keywordsResult);
            }

        } else {
            displayChatbotMessage(`파일 업로드 실패: ${result.message}`, false);
        }
    } catch (error) {
        console.error("❌ 파일 업로드 오류:", error);
        displayChatbotMessage("파일 업로드 중 오류가 발생했습니다.", false);
    }
});