import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.text_cleaner import clean_text

def preprocess(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    
    # Dataset cần có cột 'text' và 'label' (0=negative, 1=neutral, 2=positive)
    print(f"Tổng số mẫu: {len(df)}")
    print(f"Phân phối nhãn:\n{df['label'].value_counts()}")
    
    df = df.dropna(subset=['text', 'label'])
    df['text'] = df['text'].apply(clean_text)
    df = df[df['text'].str.len() > 5]  # Loại câu quá ngắn
    
    df.to_csv(output_path, index=False)
    print(f"Đã lưu {len(df)} mẫu vào {output_path}")

if __name__ == "__main__":
    preprocess(
        "dataset/raw/sentiment_dataset.csv",
        "dataset/processed/cleaned_dataset.csv"
    )