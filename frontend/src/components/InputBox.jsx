import { useState } from "react";

export default function InputBox({ onAnalyze, loading }) {
  const [text, setText] = useState("");

  const handleSubmit = () => {
    if (text.trim()) onAnalyze(text);
  };

  return (
    <div className="input-box">
      <textarea value={text} onChange={e => setText(e.target.value)} placeholder="Nhập văn bản tiếng Việt cần phân tích..." rows={5} />
      <button onClick={handleSubmit} disabled={loading || !text.trim()}>
        {loading ? "Đang phân tích..." : "Phân tích cảm xúc"}
      </button>
    </div>
  );
}
