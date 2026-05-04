# 🇻🇳 Sentiment Analysis với PhoBERT

Hệ thống phân tích cảm xúc tiếng Việt cho review sản phẩm, sử dụng mô hình PhoBERT với kiến trúc 3 tầng: React Frontend → Node.js Backend → Python AI Service.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Node.js](https://img.shields.io/badge/Node.js-18+-green)
![React](https://img.shields.io/badge/React-18-61DAFB)
![PhoBERT](https://img.shields.io/badge/Model-PhoBERT--base--v2-orange)
![Accuracy](https://img.shields.io/badge/Accuracy-77%25-yellow)

---

## 📋 Mục lục

- [Tổng quan](#-tổng-quan)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Yêu cầu cài đặt](#-yêu-cầu-cài-đặt)
- [Hướng dẫn chạy dự án](#-hướng-dẫn-chạy-dự-án)
- [Kết quả mô hình](#-kết-quả-mô-hình)
- [API Reference](#-api-reference)
- [Lỗi thường gặp](#-lỗi-thường-gặp)

---

## 🎯 Tổng quan

Dự án xây dựng hệ thống phân tích cảm xúc tiếng Việt với 3 nhãn:

| Nhãn          | Ý nghĩa               | Ví dụ                                      |
| ------------- | --------------------- | ------------------------------------------ |
| 😊 Tích cực   | Review hài lòng       | "Sản phẩm tuyệt vời, giao hàng nhanh!"     |
| 😐 Trung tính | Review bình thường    | "Sản phẩm tạm được, không có gì đặc biệt"  |
| 😞 Tiêu cực   | Review không hài lòng | "Hàng kém chất lượng, không như quảng cáo" |

**Dataset:** 19.705 review sản phẩm tiếng Việt (Shopee/Tiki)  
**Model:** [vinai/phobert-base-v2](https://huggingface.co/vinai/phobert-base-v2)  
**Training:** Google Colab T4 GPU (~7.5 phút)

---

## 🏗️ Kiến trúc hệ thống

```
User
 │
 ▼
React (Vite)          :5173   — Giao diện người dùng
 │
 ▼
Node.js (Express)     :3000   — REST API trung gian
 │
 ▼
Python (FastAPI)      :8000   — AI inference service
 │
 ▼
PhoBERT Model                 — Phân loại cảm xúc
```

---

## 📁 Cấu trúc thư mục

```
sentiment-analysis-phobert/
│
├── frontend/                        # React + Vite
│   ├── src/
│   │   ├── api/
│   │   │   └── sentimentApi.js
│   │   ├── components/
│   │   │   ├── InputBox.jsx
│   │   │   └── ResultBox.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.js
│
├── backend/                         # Node.js + Express
│   ├── src/
│   │   ├── controllers/
│   │   │   └── sentimentController.js
│   │   ├── routes/
│   │   │   └── sentimentRoutes.js
│   │   ├── services/
│   │   │   └── pythonAIService.js
│   │   ├── app.js
│   │   └── server.js
│   ├── package.json
│   └── .env
│
├── ai-service/                      # Python + FastAPI
│   ├── dataset/
│   │   ├── raw/
│   │   │   └── sentiment_dataset.csv
│   │   └── processed/
│   ├── models/
│   │   └── phobert_sentiment/       # ← Tải từ Drive về đây
│   ├── training/
│   │   ├── build_dataset.py
│   │   ├── preprocess.py
│   │   ├── train_phobert.py
│   │   └── evaluate.py
│   ├── api/
│   │   ├── app.py
│   │   └── predictor.py
│   ├── utils/
│   │   └── text_cleaner.py
│   ├── notebooks/
│   │   └── train_colab.ipynb
│   └── requirements.txt
│
├── start.bat                        # Script chạy toàn bộ (Windows)
├── .gitignore
└── README.md
```

---

## ⚙️ Yêu cầu cài đặt

| Công cụ | Phiên bản | Kiểm tra           |
| ------- | --------- | ------------------ |
| Python  | >= 3.9    | `python --version` |
| Node.js | >= 18     | `node --version`   |
| Git     | Mới nhất  | `git --version`    |

---

## 🚀 Hướng dẫn chạy dự án

### Bước 1 — Clone repo

```bash
git clone https://github.com/your-username/projectAI.git
cd projectAI
```

### Bước 2 — Tải model về

Tải thư mục `phobert_sentiment` từ Google Drive về và đặt vào:

```
ai-service/models/phobert_sentiment/
├── config.json
├── model.safetensors
├── tokenizer.json
├── vocab.txt
└── bpe.codes
```

> 💡 Link Google Drive: `[thêm link Drive của bạn vào đây]`

### Bước 3 — Cài đặt AI Service

```bash
cd ai-service

# Tạo môi trường ảo
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt
```

### Bước 4 — Cài đặt Backend

```bash
cd backend
npm install
```

Kiểm tra file `.env`:

```env
PORT=3000
AI_SERVICE_URL=http://localhost:8000
```

### Bước 5 — Cài đặt Frontend

```bash
cd frontend
npm install
```

### Bước 6 — Chạy dự án

**Mở 3 terminal riêng**:

```bash
# Terminal 1 — AI Service
cd ai-service
source venv/Scripts/activate
cd api
uvicorn app:app --port 8000

# Terminal 2 — Backend
cd backend
npm run dev

# Terminal 3 — Frontend
cd frontend
npm run dev
```

### Bước 7 — Kiểm tra

| Service         | URL                          | Kết quả           |
| --------------- | ---------------------------- | ----------------- |
| AI Service      | http://localhost:8000/health | `{"status":"ok"}` |
| AI Service Docs | http://localhost:8000/docs   | Swagger UI        |
| Backend         | http://localhost:3000/health | `{"status":"ok"}` |
| Frontend        | http://localhost:5173        | Giao diện web     |

---

## 📊 Kết quả mô hình

| Nhãn             | Precision | Recall   | F1-score |
| ---------------- | --------- | -------- | -------- |
| Tiêu cực (NEG)   | 0.84      | 0.78     | 0.81     |
| Trung tính (NEU) | 0.67      | 0.70     | 0.68     |
| Tích cực (POS)   | 0.82      | 0.83     | 0.82     |
| **Accuracy**     |           |          | **0.77** |
| **Macro avg**    | **0.77**  | **0.77** | **0.77** |

**Thông tin training:**

- Dataset: 16.500 mẫu (sau cân bằng)
- Train/Val split: 85% / 15%
- Epochs: 4
- Batch size: 32
- Learning rate: 2e-5
- Thời gian train: ~7.5 phút (Colab T4 GPU)

---

## 📡 API Reference

### AI Service (Port 8000)

**GET** `/health`

```json
{ "status": "ok" }
```

**POST** `/predict`

Request:

```json
{
  "text": "Sản phẩm tuyệt vời, giao hàng nhanh!"
}
```

Response:

```json
{
  "input": "Sản phẩm tuyệt vời, giao hàng nhanh!",
  "label": "positive",
  "label_vi": "Tích cực",
  "confidence": 0.9707,
  "scores": {
    "negative": 0.0084,
    "neutral": 0.0209,
    "positive": 0.9707
  }
}
```

### Backend (Port 3000)

**POST** `/api/sentiment/analyze`

Request/Response: tương tự AI Service `/predict`

---

## 🔧 Lỗi thường gặp

**`FileNotFoundError: model not found`**

```bash
# Kiểm tra model đã đặt đúng thư mục chưa
ls ai-service/models/phobert_sentiment/
```

**`Cannot connect to AI Service`**

```bash
# Kiểm tra AI Service đang chạy
curl http://localhost:8000/health

# Kiểm tra file .env
cat backend/.env
```

**`CORS Error` trên Frontend**

```bash
# Kiểm tra allow_origins trong ai-service/api/app.py
# và backend/src/app.js có chứa http://localhost:5173
```

**`venv\Scripts\activate` không chạy được**

```bash
# Chạy lệnh này trong PowerShell với quyền Admin
Set-ExecutionPolicy RemoteSigned
```

---

## 🛠️ Tech Stack

| Layer      | Công nghệ                                 |
| ---------- | ----------------------------------------- |
| Frontend   | React 18, Vite, Axios                     |
| Backend    | Node.js, Express, Axios                   |
| AI Service | Python, FastAPI, Uvicorn                  |
| Model      | PhoBERT-base-v2, HuggingFace Transformers |
| Training   | Google Colab T4 GPU                       |

---

## 📝 Ghi chú

- Model được train trên dataset review sản phẩm tiếng Việt
- Hỗ trợ cả văn bản có dấu và teen code không dấu
- Nhãn Trung tính (NEU) có F1 thấp hơn do đặc thù dữ liệu — có thể cải thiện bằng cách thêm data
