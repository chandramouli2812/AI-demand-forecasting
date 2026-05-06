# AI Demand Forecasting

A full-stack demand forecasting application with a FastAPI backend and a React frontend.

## Project Overview

This repository contains:

- `backend/` — FastAPI server for data upload, preprocessing, model training, prediction, and insights
- `frontend/` — React dashboard for uploading datasets, training the model, viewing forecasts, and displaying insights

The backend uses an ARIMA model to forecast future demand and exposes endpoints consumed by the React client.

## Features

- Upload demand dataset as Excel (`.xlsx`)
- Preprocess uploaded data automatically
- Train an ARIMA forecasting model
- Generate demand predictions for future days
- Produce dataset insights using the backend service
- Visualize results in a React dashboard

## Repository Structure

- `backend/app/main.py` — FastAPI app entrypoint
- `backend/app/routes/` — API route definitions
- `backend/app/services/` — preprocessing, training, prediction, and insights logic
- `backend/requirements.txt` — backend Python dependencies
- `frontend/` — React application code and build tooling
- `frontend/src/api.js` — frontend API client configured for `http://127.0.0.1:8000/api`

## Backend Setup

1. Create and activate a virtual environment:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the FastAPI server:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://127.0.0.1:8000`.

## Frontend Setup

1. Install frontend dependencies:

```powershell
cd frontend
npm install
```

2. Start the React app:

```powershell
npm start
```

The frontend will run at `http://localhost:3000` and communicate with the backend at `http://127.0.0.1:8000/api`.

## API Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/` | API root greeting |
| GET | `/health` | Health check |
| POST | `/api/upload` | Upload Excel dataset and preprocess it |
| POST | `/api/train` | Train the forecasting model using uploaded data |
| GET | `/api/predict?days=<n>` | Predict demand for the next `n` days |
| GET | `/api/insights` | Generate dataset insights |

## Usage Flow

1. Start the backend server.
2. Start the frontend app.
3. Upload a dataset through the React UI.
4. Train the model.
5. Request forecasts and view insights.

## Notes

- The backend saves processed data to `backend/processed.csv`.
- The trained model is saved to `backend/app/data/model.pkl`.
- The React frontend expects the backend API at `http://127.0.0.1:8000/api`.

## Dependencies

- Backend: `fastapi`, `uvicorn`, `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `sqlalchemy`, `python-multipart`, `openpyxl`
- Frontend: `react`, `react-dom`, `react-scripts`, `recharts`, `@testing-library/react`, and other Create React App dependencies
