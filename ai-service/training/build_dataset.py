import pandas as pd
import re

def star_to_label(star: int) -> int:
    """Chuyển số sao thành nhãn 3 lớp."""
    if star <= 2:
        return 0   # negative
    elif star == 3:
        return 1   # neutral
    else:
        return 2   # positive

def basic_clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+', '', text)           # Xóa URL
    text = re.sub(r'[^\w\s\u00C0-\u024F]', ' ', text)  # Giữ tiếng Việt
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build(input_path: str, output_path: str, 
          text_col: str, star_col: str):
    df = pd.read_csv(input_path)
    
    # Đổi tên cột cho chuẩn
    df = df.rename(columns={text_col: 'text', star_col: 'star'})
    df = df[['text', 'star']].dropna()

    # Làm sạch sơ bộ
    df['text'] = df['text'].apply(basic_clean)
    df = df[df['text'].str.len() > 10]           # Loại câu quá ngắn

    # Tạo nhãn
    df['label'] = df['star'].astype(int).apply(star_to_label)
    df = df[['text', 'label']]

    # Kiểm tra phân phối
    print("Phân phối nhãn:")
    print(df['label'].value_counts().sort_index()
          .rename({0:'Tiêu cực', 1:'Trung tính', 2:'Tích cực'}))
    
    df.to_csv(output_path, index=False)
    print(f"\nLưu {len(df)} mẫu → {output_path}")

if __name__ == "__main__":
    build(
        input_path="dataset/raw/sentiment_dataset.csv",
        output_path="dataset/raw/labeled_dataset.csv",
        text_col="comment",   # ← đổi theo tên cột thực tế của bạn
        star_col="rating"     # ← đổi theo tên cột thực tế của bạn
    )