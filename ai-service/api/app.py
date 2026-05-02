from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from predictor import SentimentPredictor

app = FastAPI(title="PhoBERT Sentiment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model 1 lần khi khởi động
predictor = SentimentPredictor()

class TextInput(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(body: TextInput):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text không được để trống")
    result = predictor.predict(body.text)
    return {"input": body.text, **result}