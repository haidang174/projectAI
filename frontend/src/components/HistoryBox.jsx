import { useEffect, useState } from "react";
import { getHistory } from "../api/sentimentApi";

const COLOR = { positive: "#22c55e", neutral: "#f59e0b", negative: "#ef4444" };

export default function HistoryBox({ refresh }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, [refresh]); // Tự reload mỗi khi có phân tích mới

  async function fetchHistory() {
    setLoading(true);
    try {
      const data = await getHistory();
      setHistory(data);
    } catch {
      console.error("Không thể tải lịch sử");
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <p className="history-loading">Đang tải lịch sử...</p>;
  if (!history.length) return null;

  return (
    <div className="history-box">
      <h3>Lịch sử phân tích</h3>
      <ul>
        {history.map(item => (
          <li key={item.id} className="history-item">
            <span className="history-badge" style={{ background: COLOR[item.label] ?? "#888" }}>
              {item.label_vi}
            </span>
            <span className="history-text">{item.input_text}</span>
            <span className="history-conf">{(item.confidence * 100).toFixed(1)}%</span>
            <span className="history-time">{new Date(item.created_at).toLocaleTimeString("vi-VN")}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
