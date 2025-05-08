from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import *
from model.mercado import Comercio

router = APIRouter(
    prefix="/comercio",
    tags=["comercio"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar/")
def create_comercio(comercio: Comercio, session=Depends(get_session)):
    return create_item(comercio, Comercio, session)


@router.patch("/atualizar/")
def update_comercio(comercio: Comercio, session=Depends(get_session)) -> Comercio:
    return update_item(comercio, Comercio, session)


@router.get("/obter/{item_id}")
def get_comercio(item_id: int, session=Depends(get_session)) -> Comercio:
    return get_item(item_id, Comercio, session)


@router.delete("/excluir/{item_id}")
def delete_comercio(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, Comercio, session)


@router.get("/comercio_por_ano/{ano}")
def get_comercio_por_ano(ano: int, session=Depends(get_session)) -> List[Comercio]:
    return get_by_field(ano, Comercio.ano, Comercio, session)


@router.get("/comercio_por_periodo/")
def get_comercio_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[Comercio]:
    return filter_by_period(ate, apos, Comercio.ano, Comercio, session)
