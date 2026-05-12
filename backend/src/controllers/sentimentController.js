const { analyzeSentiment } = require("../services/pythonAIService");
const { saveAnalysis } = require("../services/historyService");

async function analyze(req, res) {
  try {
    const { text } = req.body;
    if (!text?.trim()) {
      return res.status(400).json({ error: "Vui lòng nhập văn bản" });
    }

    // Gọi AI Service
    const result = await analyzeSentiment(text);

    // Lưu vào database
    const historyId = await saveAnalysis(text, result);

    res.json({ ...result, historyId });
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: "Lỗi khi phân tích cảm xúc" });
  }
}

module.exports = { analyze };
