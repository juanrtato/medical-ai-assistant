import uvicorn
from fastapi import FastAPI

from backend.app.api.router import api_router

app = FastAPI(
    title="Emermedica AI API",
    description="API Backend para servicios de IA de Emermédica",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a Emermédica AI API", "status": "online"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
