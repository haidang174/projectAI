import torch
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer
)
from datasets import Dataset

MODEL_NAME = "vinai/phobert-base-v2"
OUTPUT_DIR = "models/phobert_sentiment"
NUM_LABELS = 3  # negative, neutral, positive
MAX_LENGTH = 256

def load_data():
    df = pd.read_csv("dataset/processed/cleaned_dataset.csv")

    # drop null
    df = df.dropna(subset=["text", "label"])

    # bỏ cột thừa
    if "rate" in df.columns:
        df = df.drop(columns=["rate"])

    # map label string → int
    label_map = {
        "NEG": 0,
        "NEU": 1,
        "POS": 2
    }
    df["label"] = df["label"].map(label_map)

    # ép kiểu
    df["label"] = df["label"].astype(int)
    df["text"] = df["text"].astype(str)

    # split
    train_df, val_df = train_test_split(
        df,
        test_size=0.15,
        stratify=df["label"],
        random_state=42
    )

    # reset + remove index noise
    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)

    return (
        Dataset.from_pandas(train_df, preserve_index=False),
        Dataset.from_pandas(val_df, preserve_index=False)
    )

def tokenize(examples, tokenizer):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH
    )

def compute_metrics(eval_pred):
    from sklearn.metrics import accuracy_score, f1_score
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="weighted")
    }

def train():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=NUM_LABELS
    )
    
    train_ds, val_ds = load_data()
    train_ds = train_ds.map(lambda x: tokenize(x, tokenizer), batched=True)
    val_ds = val_ds.map(lambda x: tokenize(x, tokenizer), batched=True)
    
    train_ds = train_ds.remove_columns(["text"])
    val_ds = val_ds.remove_columns(["text"])
    
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        fp16=torch.cuda.is_available(),
        report_to="none"
    )
    
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    
    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Model đã lưu tại {OUTPUT_DIR}")

if __name__ == "__main__":
    train()