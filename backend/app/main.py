from contextlib import asynccontextmanager
import uvicorn
from app.api.router import api_router
from app.core.exceptions import register_exception_handlers
from app.rag.loader import ensure_vectorstore_indexed
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_vectorstore_indexed()
    yield


app = FastAPI(
    title="Emermedica AI API",
    description="API Backend para servicios de IA de Emermédica",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a Emermédica AI API", "status": "online"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    register_exception_handlers(app)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
