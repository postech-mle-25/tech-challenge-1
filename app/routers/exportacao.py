from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import create_item, delete_item, get_by_field, get_item, update_item
from model.tables import Exporta

router = APIRouter(
    prefix="/exportacao",
    tags=["exportacao"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar/")
def create(exporta: Exporta, session=Depends(get_session)):
    return create_item(exporta, Exporta, session)


@router.patch("/atualizar/")
def update_exporta(exporta: Exporta, session=Depends(get_session)) -> Exporta:
    return update_item(exporta, Exporta, session)


@router.get("/obter/{item_id}")
def get_exporta(item_id: int, session=Depends(get_session)) -> Exporta:
    return get_item(item_id, Exporta, session)


@router.delete("/excluir/{item_id}")
def delete_exporta(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, Exporta, session)


@router.get("/exporta_por_ano/{ano}")
def get_exporta_por_ano(ano: str, session=Depends(get_session)) -> List[Exporta]:
    return get_by_field(ano, Exporta.ano, Exporta, session)
