import pandas as pd

df = pd.read_csv("dataset/raw/sentiment_dataset.csv")

print("=== CÁC CỘT ===")
print(df.columns.tolist())

print("\n=== 5 DÒNG ĐẦU ===")
print(df.head())

print("\n=== GIÁ TRỊ CỘT LABEL ===")
print(df['label'].value_counts())

print("\n=== GIÁ TRỊ CỘT STAR ===")
print(df['rate'].value_counts().sort_index())

print("\n=== KIỂM TRA NULL ===")
print(df.isnull().sum())