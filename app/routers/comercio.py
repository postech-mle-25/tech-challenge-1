from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import SQLModel

from app.auth import get_current_user
from app.db import get_session
from app.model.tables import Comercio
from app.routers.base_routers import BaseRouters

router = APIRouter(
    prefix="/comercio",
    tags=["comercio"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/criar/")
def create_comercio(comercio: Comercio, session=Depends(get_session)) -> dict:
    return BaseRouters.create(comercio, Comercio, session)

@router.patch("/atualizar/")
def update_comercio(comercio: Comercio, session=Depends(get_session)) -> Comercio:
    return BaseRouters.update(comercio, Comercio, session)

@router.get("/obter/")
def get_comercio(item_id: int, session=Depends(get_session)) -> type[SQLModel]:
    return BaseRouters.get(item_id, Comercio, session)

@router.delete("/excluir/")
def delete_comercio(item_id: int, session=Depends(get_session)) -> dict:
    return BaseRouters.delete(item_id, Comercio, session)

@router.get("/comercio_por_ano/")
def get_comercio_por_ano(ano: int, session=Depends(get_session)) -> List[Comercio]:
    return BaseRouters.get_by_field(ano, Comercio.ano, Comercio, session)

@router.get("/comercio_por_periodo/")
def get_comercio_por_periodo(apos: int, ate: int, session=Depends(get_session)) -> List[Comercio]:
    return BaseRouters.filter_by_period(ate, apos, Comercio.ano, Comercio, session)

@router.get("/comercio_por_produto/")
def get_comercio_por_produto(produto: str, session=Depends(get_session)) -> List[Comercio]:
    return BaseRouters.get_by_field(produto, Comercio.produto, Comercio, session)
