from contextlib import asynccontextmanager
from fastapi import HTTPException
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import  Session
from db import get_session, create_db_and_tables
from routers import processamento

import auth
from auth import db_dependency, user_dependency


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# app.include_router(exportacao.router)
# app.include_router(importacao.router)
# app.include_router(geral.router)
app.include_router(processamento.router)
app.include_router(auth.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     #dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

@app.get("/")
async def root(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"User": user}