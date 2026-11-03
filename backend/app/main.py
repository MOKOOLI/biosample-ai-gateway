from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes_samples import router as samples_router
from app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # ساخت جدول‌ها موقع بالا اومدن سرور
    yield

app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(samples_router, prefix="/api/samples", tags=["samples"])

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name}