# AI-Based Demand Forecasting & Intelligent Inventory Optimization System

An end-to-end AI-powered forecasting and analytics platform that predicts future product demand, detects anomalies, and provides intelligent inventory recommendations using Machine Learning and Time-Series Forecasting techniques.

## 🚀 Project Overview

This project was developed as part of an advanced AI/ML evaluation assignment focused on:

* Demand Forecasting
* Inventory Optimization
* Anomaly Detection
* Automated Analytics
* Multi-Product Forecasting
* Model Monitoring

The system allows businesses to analyze historical sales data, forecast future demand, optimize inventory decisions, and detect unusual demand behavior through an interactive dashboard.

---

## 🔗 GitHub Repository

[AI-demand-forecasting Repository](https://github.com/chandramouli2812/AI-demand-forecasting?utm_source=chatgpt.com)

---

# ✨ Features

## 1. Demand Forecasting

* Forecast demand for the next:

  * 7 Days
  * 30 Days
* Supports:

  * Single Product Forecasting
  * Multi-Product Forecasting
* Uses Machine Learning / Time-Series models:

  * Linear Regression
  * ARIMA / Prophet 
---

## 2. Inventory Recommendation Engine

The system automatically calculates:

* Recommended Stock Levels
* Safety Stock
* Reorder Alerts
* Suggested Reorder Quantity

### Benefits

* Prevents stock shortages
* Reduces overstocking
* Improves operational efficiency

---

## 3. Anomaly Detection

Detects unusual demand patterns such as:

* Sudden sales spikes
* Unexpected demand drops
* Seasonal irregularities

### Techniques Used

* Z-Score Detection
* Isolation Forest (if implemented)
* Statistical Thresholding

Anomalies are highlighted visually on charts.

---

## 4. Advanced Analytics Dashboard

Interactive dashboard built using React and chart libraries.

### Dashboard Includes

* Historical Demand Trends
* Forecasted Demand Graphs
* Forecast vs Actual Comparison
* Product-wise Analytics
* Inventory Recommendations
* Anomaly Visualization
* Performance Metrics

---

## 5. Automated Retraining Workflow

The system supports:

* Retraining models on new dataset uploads
* Maintaining latest trained model
* Tracking model metadata:

  * Last trained timestamp
  * Dataset size
  * Accuracy metrics

---

## 6. Model Performance Monitoring

Evaluation metrics implemented:

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* MAPE (Mean Absolute Percentage Error)

Used for monitoring forecasting quality.

---

# 🏗️ Tech Stack

## Backend

* Python
* FastAPI

## Frontend

* React.js
* Recharts / Chart.js

## Database

* SQLite / PostgreSQL

## Machine Learning Libraries

* Pandas
* NumPy
* Scikit-learn
* Statsmodels / Prophet

---

# 📂 Project Structure

```bash
AI-demand-forecasting/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── database/
│   │   ├── forecasting/
│   │   ├── anomaly_detection/
│   │   └── inventory/
│   │
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── charts/
│   │   └── services/
│   │
│   ├── package.json
│   └── public/
│
├── datasets/
├── screenshots/
├── README.md
└── .gitignore
```

---

# 📊 Dataset Information

The dataset contains historical demand/sales information including:

| Column   | Description            |
| -------- | ---------------------- |
| Date     | Sales/Demand date      |
| Product  | Product or category    |
| Quantity | Quantity sold          |
| Store    | Store/Location details |

The dataset may be:

* Publicly available
* Synthetic/generated for testing

---

# 🤖 Forecasting Model

## Model Selection

The forecasting system uses:

* Linear Regression for trend-based forecasting
  OR
* ARIMA / Prophet for time-series forecasting

### Why This Model?

* Handles time-series demand prediction effectively
* Suitable for trend analysis
* Works well on historical sales data
* Easy integration with backend APIs

---

# 📈 Inventory Recommendation Logic

The inventory engine calculates stock recommendations using forecasted demand.

## Formula Concepts

### Safety Stock

```text
Safety Stock = Average Demand × Safety Days
```

### Reorder Point

```text
Reorder Point = Lead Time Demand + Safety Stock
```

### Suggested Reorder Quantity

```text
Reorder Quantity = Forecasted Demand - Current Inventory
```

---

# 🚨 Anomaly Detection Methodology

The system identifies abnormal demand behavior using statistical methods.

## Techniques

* Z-score based anomaly detection
* Isolation Forest (optional)

### Examples of Anomalies

* Sudden spikes in sales
* Unexpected drops
* Outlier demand periods

---

# 🔄 Automated Retraining Workflow

Whenever a new dataset is uploaded:

1. Data is validated
2. Preprocessing is applied
3. Existing model is retrained
4. New metrics are calculated
5. Metadata is stored

This ensures the forecasting model stays updated with latest demand patterns.

---

# 🔌 API Endpoints

## Dataset Upload

```http
POST /upload
```

## Train Forecasting Model

```http
POST /train
```

## Get Predictions

```http
GET /predict
```

## Get Analytics

```http
GET /analytics
```

## Inventory Recommendations

```http
GET /inventory
```

## Detect Anomalies

```http
GET /anomalies
```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/chandramouli2812/AI-demand-forecasting.git
cd AI-demand-forecasting
```

---

## 2. Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

## 3. Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs at:

```bash
http://localhost:3000
```

---

# 📷 Dashboard Features

The frontend dashboard provides:

✅ Historical Demand Visualization
✅ Forecast Graphs
✅ Forecast vs Actual Comparison
✅ Product Selection
✅ Inventory Insights
✅ Anomaly Highlighting
✅ Model Metrics Display

---

# 🧠 Edge Cases Handled

The system handles:

* Missing timestamps
* Sparse product data
* Small datasets
* Invalid file formats
* Missing values
* Sudden demand fluctuations

---

# 📌 Future Improvements

Potential enhancements:

* Hyperparameter tuning
* Model versioning
* Background training jobs
* Docker deployment
* PDF/CSV analytics export
* Real-time forecasting
* Cloud deployment

---

# 📊 Evaluation Metrics

| Metric | Purpose                               |
| ------ | ------------------------------------- |
| MAE    | Average prediction error              |
| RMSE   | Penalizes large forecasting errors    |
| MAPE   | Percentage-based forecasting accuracy |

---

# 🎯 Key Learnings

Through this project:

* Built end-to-end ML pipeline
* Integrated ML models with FastAPI
* Developed scalable backend APIs
* Created interactive analytics dashboards
* Implemented anomaly detection systems
* Learned operational AI workflows

---

# 👨‍💻 Author

**Chandramouli**

* Data Science & AI Enthusiast
* Full Stack & Machine Learning Developer

GitHub:
[Chandramouli GitHub Profile](https://github.com/chandramouli2812?utm_source=chatgpt.com)

---

# 📄 License

This project is developed for educational and evaluation purposes.
