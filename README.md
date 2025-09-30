# ⚡ Energenius – Smart Energy Management Platform

Energenius is a cost-effective, AI-powered energy management solution designed for **SMEs and factories**.  
It leverages an **ESP32 SmartBox**, **Non-Intrusive Load Monitoring (NILM)**, and **AI models** to transform aggregated energy data into actionable machine-level insights.  

With Energenius, industries can:
- Monitor energy consumption at both factory and machine levels.  
- Detect inefficiencies, overloads, and potential faults early.  
- Receive plain-language insights via a **dashboard** and a **chatbot assistant**.  
- (Future) Automatically optimize machine operations through agentic AI.  

---

## 📌 Features

- **SmartBox Acquisition:** ESP32-based device collects aggregate energy data using PZEM sensors, no invasive installation required.  
- **NILM Disaggregation:** LSTM-based models break down aggregate usage into per-machine consumption.  
- **Classification:** AI models (PyTorch & TensorFlow) detect inefficiencies, fault risks, and predict maintenance needs.  
- **Dashboard:** Web app (HTML/CSS/JS frontend, Node.js + Flask backend) for visualization, analytics, and reports.  
- **Chatbot Assistant:** Conversational AI layer (RAG pipeline + Grok API) provides natural-language explanations and recommendations.  
- **Future Agentic Optimization:** Autonomous workload scheduling and energy-saving actions.  

---

## 🏗️ System Architecture

1. **Edge Layer**  
   - ESP32 SmartBox + PZEM sensors (C++ / WiFi.h).  
   - Sends data via WebSocket to the cloud.  

2. **Ingestion Layer**  
   - Flask API handles data ingestion from ESP32.  
   - Data stored in MongoDB for persistence and analytics.  

3. **AI Layer**  
   - NILM with PyTorch LSTMs.  
   - Classification models with PyTorch + TensorFlow.  
   - Data preprocessing with NumPy, pandas, scikit-learn.  

4. **Application Layer**  
   - Dashboard: HTML, CSS, JS, Node.js, Flask.  
   - Chatbot: RAG over datasets + Grok API.  

---

## 🛠️ Technology Stack

- **Hardware:** ESP32, PZEM sensors (C++ / WiFi.h).  
- **AI/ML:** PyTorch, TensorFlow, NumPy, pandas, scikit-learn, Plotly.  
- **Backend:** Python (Flask), Node.js.  
- **Database:** MongoDB.  
- **Frontend:** HTML, CSS, JavaScript.  
- **Chatbot:** Static RAG pipeline + Grok API.  

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+  
- Node.js 16+  
- ESP32 board + PZEM sensors (for hardware testing)  
- MongoDB instance  

### Installation

```bash
# Clone the repository
git clone https://github.com/Leb0wsKy/Appliance-energy-prediction.git
cd Appliance-energy-prediction

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for dashboard)
cd dashboard
npm install
