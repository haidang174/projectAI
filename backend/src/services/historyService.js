const db = require('../config/db');

// Lưu kết quả phân tích
async function saveAnalysis(inputText, result) {
    const { label, label_vi, confidence, scores } = result;
    const [row] = await db.execute(
        `INSERT INTO analysis_history 
         (input_text, label, label_vi, confidence, score_pos, score_neu, score_neg)
         VALUES (?, ?, ?, ?, ?, ?, ?)`,
        [inputText, label, label_vi, confidence,
         scores.positive, scores.neutral, scores.negative]
    );

    // Cập nhật thống kê theo ngày
    await updateStatistics(label);

    return row.insertId;
}

// Cập nhật bảng statistics
async function updateStatistics(label) {
    const today = new Date().toISOString().split('T')[0];
    const colMap = {
        positive: 'count_pos',
        neutral:  'count_neu',
        negative: 'count_neg'
    };
    const col = colMap[label] || 'count_neu';

    await db.execute(
        `INSERT INTO statistics (date, total, ${col})
         VALUES (?, 1, 1)
         ON DUPLICATE KEY UPDATE
         total = total + 1,
         ${col} = ${col} + 1`,
        [today]
    );
}

// Lưu feedback người dùng
async function saveFeedback(historyId, isCorrect, correctLabel = null) {
    await db.execute(
        `INSERT INTO feedback (history_id, is_correct, correct_label)
         VALUES (?, ?, ?)`,
        [historyId, isCorrect, correctLabel]
    );
}

// Lấy lịch sử (10 cái gần nhất)
async function getHistory(limit = 10) {
    const [rows] = await db.execute(
        `SELECT id, input_text, label_vi, confidence, created_at
         FROM analysis_history
         ORDER BY created_at DESC
         LIMIT ?`,
        [limit]
    );
    return rows;
}

// Lấy thống kê 7 ngày gần nhất
async function getStatistics() {
    const [rows] = await db.execute(
        `SELECT date, total, count_pos, count_neu, count_neg
         FROM statistics
         ORDER BY date DESC
         LIMIT 7`
    );
    return rows;
}

module.exports = { saveAnalysis, saveFeedback, getHistory, getStatistics };