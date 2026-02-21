"""FastAPI application entry point."""
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LatSpace AI backend starting up...")
    logger.info(f"Gemini model: {os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')}")
    yield
    logger.info("LatSpace AI backend shutting down.")


app = FastAPI(
    title="LatSpace AI Platform",
    description="Intelligent Excel Parser (Track A) + Parameter Onboarding Wizard (Track B)",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import track_a, track_b  # noqa: E402

app.include_router(track_a.router)
app.include_router(track_b.router)


@app.get("/health", tags=["Meta"])
def health() -> dict:
    return {"status": "ok", "version": "1.0.0"}