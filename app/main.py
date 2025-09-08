from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.api.v1.routes import router as api_v1_router
from app.core.config import settings
from app.core.db import async_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    if settings.ENV == "development":
        # async with async_engine.begin() as conn:
        #     await conn.run_sync(SQLModel.metadata.create_all)
        pass
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # allow Authorization, Content-Type, etc.
)

app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health():
    return {"status": "ok"}
