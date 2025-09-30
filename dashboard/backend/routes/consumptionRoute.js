import express from "express";
import mongoose from "mongoose";
import Measurement from "../models/Measurement.js";

const router = express.Router();

// GET /api/total-consumption/:userId
router.get("/total-consumption/:userId", async (req, res) => {
  const { userId } = req.params;

  if (!mongoose.Types.ObjectId.isValid(userId)) {
    return res.status(400).json({ error: "userId invalide" });
  }

  try {
    const measurements = await Measurement.find({ userId }).sort({ timestamp: 1 });

    if (!measurements.length) {
      return res.status(200).json({
        userId,
        totalConsumption_kWh: 0,
        count: 0,
      });
    }

    let totalEnergy = 0;

    for (let i = 1; i < measurements.length; i++) {
      const prev = measurements[i - 1];
      const curr = measurements[i];

      const deltaHours = (new Date(curr.timestamp) - new Date(prev.timestamp)) / 1000 / 3600;

      totalEnergy += prev.globalConsumption * deltaHours;
    }

    res.status(200).json({
      userId,
      totalConsumption_kWh: totalEnergy,
      count: measurements.length,
    });
  } catch (error) {
    console.error("Erreur total-consumption:", error);
    res.status(500).json({ error: "Erreur serveur" });
  }
});

export default router;
