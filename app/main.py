import asyncio
import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from app import auth
from app.auth import user_dependency
from app.db import create_db_and_tables, get_session
from app.routers import comercio, exportacao, importacao, processamento, producao
from etl.ingestion_df import db_ingestion


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

async def main():
    config = uvicorn.Config("main:app", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
