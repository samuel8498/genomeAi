from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.predict import router as predict_router

app = FastAPI(
    title="GenomeAI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)

@app.get("/")
def home():
    return {
        "message":"GenomeAI API Running Successfully"
    }