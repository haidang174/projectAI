import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
from pathlib import Path

# Đường dẫn tương đối từ thư mục ai-service
MODEL_DIR = Path(__file__).parent.parent / "models" / "phobert_sentiment"

LABELS    = {0: "negative", 1: "neutral",  2: "positive"}
LABELS_VI = {0: "Tiêu cực", 1: "Trung tính", 2: "Tích cực"}

def clean_text(text: str) -> str:
    if not isinstance(text, str): return ""
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s\u00C0-\u024F]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

class SentimentPredictor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading model from {MODEL_DIR}...")
        self.tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
        self.model     = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR))
        self.model.to(self.device)
        self.model.eval()
        print(f"Model loaded on {self.device}")

    def predict(self, text: str) -> dict:
        cleaned = clean_text(text)
        inputs  = self.tokenizer(
            cleaned, return_tensors="pt",
            truncation=True, max_length=128
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs    = torch.softmax(logits, dim=-1)[0].tolist()
        pred_idx = int(torch.argmax(logits).item())

        return {
            "label":      LABELS[pred_idx],
            "label_vi":   LABELS_VI[pred_idx],
            "confidence": round(probs[pred_idx], 4),
            "scores": {
                "negative": round(probs[0], 4),
                "neutral":  round(probs[1], 4),
                "positive": round(probs[2], 4),
            }
        }