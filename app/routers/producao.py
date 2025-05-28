from typing import List

from app.auth import get_current_user
from app.db import get_session
from fastapi import APIRouter, Depends
from app.model.base_queries import filter_by_period
from app.model.tables import Producao
from app.routers.base_routers import BaseRouters

router = APIRouter(
    prefix="/producao",
    tags=["producao"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar/")
def create_producao(producao: Producao, session=Depends(get_session)):
    return BaseRouters.create(producao, Producao, session)


@router.patch("/atualizar/")
def update_producao(producao: Producao, session=Depends(get_session)) -> Producao:
    return BaseRouters.update(producao, Producao, session)


@router.get("/obter/")
def get_producao(item_id: int, session=Depends(get_session)) -> Producao:
    return BaseRouters.get(item_id, Producao, session)


# @router.get("/{tipo}")
# def get_producao_por_tipo(tipo: str, session=Depends(get_session)) -> List[Producao]:
#     return BaseRouters.get_by_field(tipo, Producao.tipo, Producao, session)


@router.delete("/excluir/")
def delete_producao(item_id: int, session=Depends(get_session)):
    return BaseRouters.delete(item_id, Producao, session)


@router.get("/producao_por_ano/")
def get_producao_por_ano(ano: int, session=Depends(get_session)) -> List[Producao]:
    return BaseRouters.get_by_field(ano, Producao.ano, Producao, session)


@router.get("/producao_por_periodo/")
def get_producao_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[Producao]:
    return filter_by_period(ate, apos, Producao.ano, Producao, session)
