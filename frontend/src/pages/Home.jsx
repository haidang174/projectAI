import { useState } from "react";
import InputBox from "../components/InputBox";
import ResultBox from "../components/ResultBox";
import { analyzeSentiment } from "../api/sentimentApi";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async text => {
    setLoading(true);
    setError("");
    try {
      const data = await analyzeSentiment(text);
      setResult(data);
    } catch {
      setError("Không thể kết nối đến server. Vui lòng thử lại.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>Phân tích cảm xúc tiếng Việt</h1>
      <p className="subtitle">Powered by PhoBERT</p>
      <InputBox onAnalyze={handleAnalyze} loading={loading} />
      {error && <p className="error">{error}</p>}
      <ResultBox result={result} />
    </main>
  );
}
