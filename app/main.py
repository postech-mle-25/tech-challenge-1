from contextlib import asynccontextmanager
from fastapi import HTTPException, Depends, FastAPI
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session

from app.db import get_session, create_db_and_tables
from app.routers.ingestion import router as ingestion_router
from app.routers import processamento

import auth
from auth import db_dependency, user_dependency


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado no startup
    create_db_and_tables()
    yield
    # Código executado no shutdown (se necessário)
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)
SessionDep = Annotated[Session, Depends(get_session)]


# app.include_router(exportacao.router)
# app.include_router(importacao.router)
# app.include_router(geral.router)
# app.include_router(processamento.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     #dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


app.include_router(ingestion_router, prefix = '/api')
app.include_router(processamento.router)
app.include_router(auth.router)


@app.get("/")
async def root(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"User": user}