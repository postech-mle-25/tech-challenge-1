from fastapi import HTTPException, Depends, FastAPI
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session

from app.db import get_session, create_db_and_tables
from app.routers import comercio, exportacao, importacao, producao, processamento
from app.etl.ingestion_df import db_ingestion

from app import auth
from app.auth import db_dependency, user_dependency


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado no startup
    create_db_and_tables()
    db_ingestion()
    yield
    # Código executado no shutdown (se necessário)
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)
SessionDep = Annotated[Session, Depends(get_session)]

app.include_router(auth.router)
app.include_router(processamento.router, prefix = '/api')
app.include_router(comercio.router, prefix='/api')
app.include_router(exportacao.router, prefix='/api')
app.include_router(importacao.router, prefix='/api')
app.include_router(producao.router, prefix='/api')

@app.get("/")
async def root(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"User": user}