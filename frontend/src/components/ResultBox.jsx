const COLOR = { positive: "#22c55e", neutral: "#f59e0b", negative: "#ef4444" };

export default function ResultBox({ result }) {
  if (!result) return null;
  const { label, label_vi, confidence, scores } = result;

  return (
    <div className="result-box" style={{ borderColor: COLOR[label] }}>
      <h2>{label_vi}</h2>
      <p>
        Độ tin cậy: <strong>{(confidence * 100).toFixed(1)}%</strong>
      </p>
      <div className="scores">
        {Object.entries(scores).map(([k, v]) => (
          <div key={k} className="score-bar">
            <span>{k}</span>
            <div className="bar">
              <div style={{ width: `${v * 100}%`, background: COLOR[k] }} />
            </div>
            <span>{(v * 100).toFixed(1)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
