from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import create_item, delete_item, get_by_field, get_item, update_item
from model.importacao import *

router = APIRouter(
    prefix="/importacao",
    tags=["importacao"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar_fresca/")
def create_fresca(fresca: ImpFrescas, session=Depends(get_session)):
    return create_item(fresca, ImpFrescas, session)


@router.patch("/atualizar_fresca/")
def update_fresca(fresca: ImpFrescas, session=Depends(get_session)) -> ImpFrescas:
    return update_item(fresca, ImpFrescas, session)


@router.get("/obter_fresca/{item_id}")
def get_fresca(item_id: int, session=Depends(get_session)) -> ImpFrescas:
    return get_item(item_id, ImpFrescas, session)


@router.delete("/excluir_fresca/{item_id}")
def delete_fresca(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ImpFrescas, session)


@router.get("/frescas_por_ano/{ano}")
def get_frescas_por_ano(ano: str, session=Depends(get_session)) -> List[ImpFrescas]:
    return get_by_field(ano, ImpFrescas.ano, ImpFrescas, session)


@router.post("/criar_passa/")
def create_passa(passa: ImpPassas, session=Depends(get_session)):
    return create_item(passa, ImpPassas, session)


@router.patch("/atualizar_passa/")
def update_passa(passa: ImpPassas, session=Depends(get_session)) -> ImpPassas:
    return update_item(passa, ImpPassas, session)


@router.get("/obter_passa/{item_id}")
def get_passa(item_id: int, session=Depends(get_session)) -> ImpPassas:
    return get_item(item_id, ImpPassas, session)


@router.delete("/excluir_passa/{item_id}")
def delete_passa(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ImpPassas, session)


@router.get("/passas_por_ano/{ano}")
def get_passas_por_ano(ano: str, session=Depends(get_session)) -> List[ImpPassas]:
    return get_by_field(ano, ImpPassas.ano, ImpPassas, session)


@router.post("/criar_suco/")
def create_suco(suco: ImpSuco, session=Depends(get_session)):
    return create_item(suco, ImpSuco, session)


@router.patch("/atualizar_suco/")
def update_suco(suco: ImpSuco, session=Depends(get_session)) -> ImpSuco:
    return update_item(suco, ImpSuco, session)


@router.get("/obter_suco/{item_id}")
def get_suco(item_id: int, session=Depends(get_session)) -> ImpSuco:
    return get_item(item_id, ImpSuco, session)


@router.delete("/excluir_suco/{item_id}")
def delete_suco(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ImpSuco, session)


@router.get("/suco_por_ano/{ano}")
def get_suco_por_ano(ano: str, session=Depends(get_session)) -> List[ImpSuco]:
    return get_by_field(ano, ImpSuco.ano, ImpSuco, session)


@router.post("/criar_vinho/")
def create_vinho(vinho: ImpVinhos, session=Depends(get_session)):
    return create_item(vinho, ImpVinhos, session)


@router.patch("/atualizar_vinho/")
def update_vinho(vinho: ImpVinhos, session=Depends(get_session)) -> ImpVinhos:
    return update_item(vinho, ImpVinhos, session)


@router.get("/obter_vinho/{item_id}")
def get_vinho(item_id: int, session=Depends(get_session)) -> ImpVinhos:
    return get_item(item_id, ImpVinhos, session)


@router.delete("/excluir_vinho/{item_id}")
def delete_vinho(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ImpVinhos, session)


@router.get("/vinho_por_ano/{ano}")
def get_vinho_por_ano(ano: str, session=Depends(get_session)) -> List[ImpVinhos]:
    return get_by_field(ano, ImpVinhos.ano, ImpVinhos, session)
