import torch
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments

# ✅ 추가 학습할 새로운 데이터셋 로드
new_train_df = pd.read_csv("./dataset/fake_real_news_10000_dataset.csv")

# ✅ 제목 + 본문을 결합하여 학습
new_train_df["text"] = new_train_df["title"] + " " + new_train_df["content"]

# ✅ Hugging Face Dataset 포맷으로 변환
new_train_dataset = Dataset.from_pandas(new_train_df[["text", "label"]])

# ✅ 기존에 사용한 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained("./models/kobert-news-finetuned")

# ✅ 데이터 토큰화 함수
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

# ✅ 데이터셋 토큰화 적용
new_train_tokenized = new_train_dataset.map(preprocess_function, batched=True)

# ✅ DatasetDict 변환 (검증 데이터는 기존 모델에 맞춰 생략 가능)
new_dataset = DatasetDict({
    "train": new_train_tokenized
})

# ✅ 기존 모델 불러오기 (이전 학습된 모델 활용)
model = BertForSequenceClassification.from_pretrained("./models/kobert-news-finetuned")

# ✅ GPU 사용 여부 확인 후 모델 이동
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# ✅ 추가 학습용 파라미터 설정
training_args = TrainingArguments(
    output_dir="./kobert-fake-news-continued",
    evaluation_strategy="no",  # 추가 학습이므로 검증 과정 생략 가능
    save_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=2,  # 기존 모델이 학습된 상태라서 너무 많은 epoch는 불필요
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=500,
    save_total_limit=2,
    fp16=True
)

# ✅ Trainer 정의
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=new_dataset["train"]
)

# ✅ 기존 모델에 추가 학습 진행
trainer.train()

# ✅ 추가 학습된 모델 저장
model.save_pretrained("./models/kobert-news-continued")
tokenizer.save_pretrained("./models/kobert-news-continued")

print("🎉 기존 모델에 추가 학습 완료! 저장 경로: ./models/kobert-news-continued")
