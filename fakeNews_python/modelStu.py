import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments

# ✅ 데이터 로드
train_df = pd.read_csv("./dataset/korean_fake_news_train.csv")
valid_df = pd.read_csv("./dataset/korean_fake_news_valid.csv")

# ✅ 데이터의 10%만 사용 (학습 속도 테스트용)
train_df = train_df.sample(frac=0.1, random_state=42)
valid_df = valid_df.sample(frac=0.1, random_state=42)


# ✅ 제목 + 본문을 결합하여 학습
train_df["text"] = train_df["title"] + " " + train_df["content"]
valid_df["text"] = valid_df["title"] + " " + valid_df["content"]

# ✅ Hugging Face Dataset 포맷으로 변환
train_dataset = Dataset.from_pandas(train_df[["text", "label"]])
valid_dataset = Dataset.from_pandas(valid_df[["text", "label"]])

# ✅ KoBERT 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained("monologg/kobert")

# ✅ 데이터 토큰화 함수
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

# ✅ 데이터셋 토큰화 적용
train_tokenized = train_dataset.map(preprocess_function, batched=True)
valid_tokenized = valid_dataset.map(preprocess_function, batched=True)

# ✅ 데이터셋 딕셔너리로 변환
dataset = DatasetDict({
    "train": train_tokenized,
    "validation": valid_tokenized
})

# ✅ KoBERT 모델 로드
model = BertForSequenceClassification.from_pretrained("monologg/kobert", num_labels=2)


# ✅ 학습 파라미터 설정
training_args = TrainingArguments(
    output_dir="./kobert-fake-news",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,  # 학습 횟수 (조정 가능)
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=500,
    save_total_limit=2
)

# ✅ Trainer 정의
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"]
)

# ✅ 모델 학습 시작
trainer.train()

# ✅ 학습 완료 후 모델 저장
model.save_pretrained("./models/kobert-news-finetuned")
tokenizer.save_pretrained("./models/kobert-news-finetuned")

print("🎉 모델 학습 완료! 저장 경로: ./models/kobert-news-finetuned")
