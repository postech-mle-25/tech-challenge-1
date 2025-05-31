from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import HTTPException, Depends, FastAPI
from sqlmodel import Session

from etl.ingestion_df import db_ingestion
from app.db import get_session, create_db_and_tables
from app.routers import comercio, exportacao, importacao, producao, processamento
from app import auth
from app.auth import user_dependency


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    db_ingestion()
    yield
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)
SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/")
async def root(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"User": user}

app.include_router(auth.router)
app.include_router(processamento.router, prefix = '/api')
app.include_router(comercio.router, prefix='/api')
app.include_router(exportacao.router, prefix='/api')
app.include_router(importacao.router, prefix='/api')
app.include_router(producao.router, prefix='/api')