from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import create_item, delete_item, get_by_field, get_item, update_item
from model.tables import Importa

router = APIRouter(
    prefix="/importacao",
    tags=["importacao"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar/")
def create_importa(importa: Importa, session=Depends(get_session)):
    return create_item(importa, Importa, session)


@router.patch("/atualizar/")
def update_importa(importa: Importa, session=Depends(get_session)) -> Importa:
    return update_item(importa, Importa, session)


@router.get("/obter/{item_id}")
def get_importa(item_id: int, session=Depends(get_session)) -> Importa:
    return get_item(item_id, Importa, session)


@router.delete("/excluir/{item_id}")
def delete_importa(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, Importa, session)


@router.get("/importas_por_ano/{ano}")
def get_importa_por_ano(ano: str, session=Depends(get_session)) -> List[Importa]:
    return get_by_field(ano, Importa.ano, Importa, session)
