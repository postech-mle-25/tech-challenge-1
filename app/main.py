from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import Session
from db import get_session, create_db_and_tables
from routers import processamento

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado no startup
    create_db_and_tables()
    yield
    # Código executado no shutdown (se necessário)
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)

# app.include_router(exportacao.router)
# app.include_router(importacao.router)
# app.include_router(geral.router)
app.include_router(processamento.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     #dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

@app.get("/")
async def root():
    return {"message": "Hello!"}