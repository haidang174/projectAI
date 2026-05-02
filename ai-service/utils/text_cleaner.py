import re
import unicodedata
from underthesea import word_tokenize

def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text)

def remove_noise(text: str) -> str:
    text = re.sub(r'http\S+|www\S+', '', text)       # URLs
    text = re.sub(r'[^\w\s\u00C0-\u024F]', ' ', text) # Ký tự đặc biệt
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_vietnamese(text: str) -> str:
    return word_tokenize(text, format="text")

def clean_text(text: str) -> str:
    text = normalize_unicode(text)
    text = remove_noise(text)
    text = tokenize_vietnamese(text)
    return text.lower()