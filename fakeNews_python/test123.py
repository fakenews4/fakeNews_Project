from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# ✅ 모델 다운로드
model_name = "ainize/kobart-news"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# ✅ 로컬 저장
model.save_pretrained("./models/kobart-news")
tokenizer.save_pretrained("./models/kobart-news")

print("✅ 모델 다운로드 및 저장 완료!")
