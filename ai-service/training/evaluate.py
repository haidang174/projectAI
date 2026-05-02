import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

MODEL_DIR = "models/phobert_sentiment"
LABEL_NAMES = ["Tiêu cực", "Trung tính", "Tích cực"]

def evaluate():
    df = pd.read_csv("dataset/processed/cleaned_dataset.csv")
    _, test_df = train_test_split(df, test_size=0.15, 
                                   stratify=df['label'], random_state=42)
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    preds = []
    for text in test_df['text'].tolist():
        inputs = tokenizer(text, return_tensors="pt", 
                          truncation=True, max_length=256).to(device)
        with torch.no_grad():
            logits = model(**inputs).logits
        preds.append(torch.argmax(logits).item())
    
    print(classification_report(test_df['label'], preds, 
                                  target_names=LABEL_NAMES))

if __name__ == "__main__":
    evaluate()