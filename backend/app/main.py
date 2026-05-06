from fastapi import FastAPI
from app.routes import upload, train, predict, insights
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload.router, prefix="/api")
app.include_router(train.router, prefix="/api")
app.include_router(predict.router, prefix="/api")
app.include_router(insights.router, prefix="/api")

# Root
@app.get("/")
def home():
    return {"message": "AI Demand Forecasting API"}

# Health Check
@app.get("/health")
def health():
    return {"status": "ok"}