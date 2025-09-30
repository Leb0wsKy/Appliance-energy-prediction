// routes/measurementRoutes.js
import express from "express";
import Measurement from "../models/Measurement.js";

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { userId, timestamp, globalConsumption, measurements } = req.body;

    if (!userId || !timestamp || !globalConsumption) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const measurement = new Measurement({
      userId,
      timestamp,
      globalConsumption,
      measurements,
    });

    await measurement.save();
    res.status(201).json({ message: "Measurement saved successfully" });
  } catch (error) {
    console.error("Error saving measurement:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});
// GET /api/measurements?userId=...
router.get("/", async (req, res) => {
  try {
    const { userId } = req.query;
    if (!userId) return res.status(400).json({ error: "userId is required" });

    const measurements = await Measurement.find({ userId }).sort({ timestamp: 1 });
    res.json(measurements);
  } catch (error) {
    console.error("Error fetching measurements:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});


export default router;
