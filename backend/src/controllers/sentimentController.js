const { analyzeSentiment } = require("../services/pythonAIService");

async function analyze(req, res) {
  try {
    const { text } = req.body;
    if (!text?.trim()) {
      return res.status(400).json({ error: "Vui lòng nhập văn bản" });
    }
    const result = await analyzeSentiment(text);
    res.json(result);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: "Lỗi khi phân tích cảm xúc" });
  }
}

module.exports = { analyze };
