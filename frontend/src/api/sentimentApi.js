import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:3000/api" });

export async function analyzeSentiment(text) {
  const { data } = await api.post("/sentiment/analyze", { text });
  return data;
}

export async function getHistory() {
  const { data } = await api.get("/sentiment/history");
  return data;
}
