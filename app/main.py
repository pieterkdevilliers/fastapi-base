from fastapi import FastAPI
from sqlmodel import SQLModel
from app.api.v1.routes import router as api_v1_router
from app.core.config import settings
from app.core.db import engine
from app.models.accounts import Account
from app.models.users import User

app = FastAPI(title=settings.PROJECT_NAME)


def init_db():
    if settings.ENV == "development":
        SQLModel.metadata.create_all(engine)

init_db()


app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health():
    return {"status": "ok"}
