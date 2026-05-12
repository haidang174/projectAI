import { useState } from "react";
import InputBox from "../components/InputBox";
import ResultBox from "../components/ResultBox";
import HistoryBox from "../components/HistoryBox";
import { analyzeSentiment } from "../api/sentimentApi";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [refresh, setRefresh] = useState(0); // Trigger reload lịch sử

  const handleAnalyze = async text => {
    setLoading(true);
    setError("");
    try {
      const data = await analyzeSentiment(text);
      setResult(data);
      setRefresh(r => r + 1); // Reload lịch sử sau mỗi lần phân tích
    } catch {
      setError("Không thể kết nối đến server. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>🇻🇳 Phân tích cảm xúc tiếng Việt</h1>
      <p className="subtitle">Powered by PhoBERT</p>
      <InputBox onAnalyze={handleAnalyze} loading={loading} />
      {error && <p className="error">{error}</p>}
      <ResultBox result={result} />
      <HistoryBox refresh={refresh} />
    </main>
  );
}
