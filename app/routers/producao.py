from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import create_item, delete_item, filter_by_period, get_by_field, get_item, update_item
from model.tables import Producao

router = APIRouter(
    prefix="/producao",
    tags=["producao"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar/")
def create_producao(producao: Producao, session=Depends(get_session)):
    return create_item(producao, Producao, session)


@router.patch("/atualizar/")
def update_producao(producao: Producao, session=Depends(get_session)) -> Producao:
    return update_item(producao, Producao, session)


@router.get("/obter/{item_id}")
def get_producao(item_id: int, session=Depends(get_session)) -> Producao:
    return get_item(item_id, Producao, session)


@router.get("/{tipo}")
def get_producao_por_tipo(tipo: str, session=Depends(get_session)) -> List[Producao]:
    return get_by_field(tipo, Producao.tipo, Producao, session)


@router.delete("/excluir/{item_id}")
def delete_producao(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, Producao, session)


@router.get("/producao_por_ano/{ano}")
def get_producao_por_ano(ano: int, session=Depends(get_session)) -> List[Producao]:
    return get_by_field(ano, Producao.ano, Producao, session)


@router.get("/producao_por_periodo/")
def get_producao_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[Producao]:
    return filter_by_period(ate, apos, Producao.ano, Producao, session)
