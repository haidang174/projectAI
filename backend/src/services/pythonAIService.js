const axios = require("axios");

const AI_URL = process.env.AI_SERVICE_URL || "http://localhost:8000";

async function analyzeSentiment(text) {
  const response = await axios.post(`${AI_URL}/predict`, { text });
  return response.data;
}

async function checkHealth() {
  const response = await axios.get(`${AI_URL}/health`);
  return response.data;
}

module.exports = { analyzeSentiment, checkHealth };
