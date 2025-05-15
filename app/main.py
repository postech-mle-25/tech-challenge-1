from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import  Session
from app.db import get_session, create_db_and_tables
from app.routers.ingestion import router as ingestion_router


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()



# app.include_router(exportacao.router)
# app.include_router(importacao.router)
# app.include_router(geral.router)
# app.include_router(processamento.router)
app.include_router(ingestion_router, prefix = '/api')

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