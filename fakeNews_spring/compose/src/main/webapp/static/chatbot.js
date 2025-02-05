const sendMessageButton = document.getElementById("send-message");
const userInput = document.getElementById("user-input");
const chatbotMessages = document.getElementById("chatbot-messages");

const crawlButton = document.getElementById("crawl-button");
const linkInput = document.getElementById("news-link");

let crawledContent = null;
let crawledUrl = null;

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

        // 크롤링 완료 메시지 바로 출력
        displayChatbotMessage(`뉴스 링크가 업로드되었습니다.`, false);
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
                // 만약 결과가 객체라면 content 필드를 사용
                if (typeof result.summary === "object" && result.summary !== null) {
                    summary = result.summary.content;
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
