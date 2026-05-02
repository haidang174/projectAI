const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const sentimentRoutes = require("./routes/sentimentRoutes");

const app = express();
app.use(cors());
app.use(morgan("dev"));
app.use(express.json());

app.use("/api/sentiment", sentimentRoutes);

app.get("/health", (_, res) => res.json({ status: "ok" }));

module.exports = app;
