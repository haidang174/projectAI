const express = require("express");
const { analyze } = require("../controllers/sentimentController");
const { getHistory, getStatistics, saveFeedback } = require("../services/historyService");

const router = express.Router();

router.post("/analyze", analyze);

// Lấy lịch sử phân tích
router.get("/history", async (req, res) => {
  try {
    const data = await getHistory();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Lỗi lấy lịch sử" });
  }
});

// Lấy thống kê
router.get("/statistics", async (req, res) => {
  try {
    const data = await getStatistics();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Lỗi lấy thống kê" });
  }
});

// Gửi feedback
router.post("/feedback", async (req, res) => {
  try {
    const { historyId, isCorrect, correctLabel } = req.body;
    await saveFeedback(historyId, isCorrect, correctLabel);
    res.json({ message: "Cảm ơn phản hồi của bạn!" });
  } catch (err) {
    res.status(500).json({ error: "Lỗi lưu feedback" });
  }
});

module.exports = router;
