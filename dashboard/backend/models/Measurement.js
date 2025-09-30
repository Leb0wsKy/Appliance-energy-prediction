import mongoose from "mongoose";

const measurementSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  timestamp: { type: Date, required: true },
  globalConsumption: { type: Number, required: true },
  measurements: { type: Object } // { Fridge: 150, Washer: 20, Microwave: 5 }
});

export default mongoose.model("Measurement", measurementSchema);
