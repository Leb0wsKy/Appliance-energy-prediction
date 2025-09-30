import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import authRoutes from "./routes/auth.js";
import measurementRoutes from "./routes/measurementRoutes.js";

import consumptionRoute from "./routes/consumptionRoute.js";


const app = express();
app.use(cors());
app.use(express.json());
// Connect to MongoDB avec site localhost:27017
mongoose.connect("mongodb://localhost:27017", {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log("MongoDB connected"))
  .catch(err => console.error("MongoDB connection error:", err));

app.use("/api/auth", authRoutes);

app.use("/api/measurements", measurementRoutes);

app.use("/api", consumptionRoute);

app.get("/", (req, res) => res.send("Server is running"));
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
