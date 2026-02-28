from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router



app = FastAPI(title="Semantica API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "tauri://localhost",
        "http://localhost:3000",
        "http://localhost",
        "https://tauri.localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Semantica API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(api_router, prefix='/api/v1')

