from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import create_item, delete_item, get_by_field, get_item, update_item
from model.exportacao import *

router = APIRouter(
    prefix="/exportacao",
    tags=["exportacao"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar_espumante/")
def create_espumante(espumante: ExpEspumantes, session=Depends(get_session)):
    return create_item(espumante, ExpEspumantes, session)


@router.patch("/atualizar_espumante/")
def update_espumante(
    espumante: ExpEspumantes, session=Depends(get_session)
) -> ExpEspumantes:
    return update_item(espumante, ExpEspumantes, session)


@router.get("/obter_espumante/{item_id}")
def get_espumante(item_id: int, session=Depends(get_session)) -> ExpEspumantes:
    return get_item(item_id, ExpEspumantes, session)


@router.delete("/excluir_espumante/{item_id}")
def delete_espumante(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ExpEspumantes, session)


@router.get("/espumante_por_ano/{ano}")
def get_espumante_por_ano(
    ano: str, session=Depends(get_session)
) -> List[ExpEspumantes]:
    return get_by_field(ano, ExpEspumantes.ano, ExpEspumantes, session)


@router.post("/criar_suco/")
def create_suco(suco: ExpSuco, session=Depends(get_session)):
    return create_item(suco, ExpSuco, session)


@router.patch("/atualizar_suco/")
def update_suco(suco: ExpSuco, session=Depends(get_session)) -> ExpSuco:
    return update_item(suco, ExpSuco, session)


@router.get("/obter_suco/{item_id}")
def get_suco(item_id: int, session=Depends(get_session)) -> ExpSuco:
    return get_item(item_id, ExpSuco, session)


@router.delete("/excluir_suco/{item_id}")
def delete_suco(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ExpSuco, session)


@router.get("/suco_por_ano/{ano}")
def get_suco_por_ano(ano: str, session=Depends(get_session)) -> List[ExpSuco]:
    return get_by_field(ano, ExpSuco.ano, ExpSuco, session)


@router.post("/criar_uva/")
def create_uva(uva: ExpUva, session=Depends(get_session)):
    return create_item(uva, ExpUva, session)


@router.patch("/atualizar_uva/")
def update_uva(uva: ExpUva, session=Depends(get_session)) -> ExpUva:
    return update_item(uva, ExpUva, session)


@router.get("/obter_uva/{item_id}")
def get_uva(item_id: int, session=Depends(get_session)) -> ExpUva:
    return get_item(item_id, ExpUva, session)


@router.delete("/excluir_uva/{item_id}")
def delete_uva(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ExpUva, session)


@router.get("/uva_por_ano/{ano}")
def get_uva_por_ano(ano: str, session=Depends(get_session)) -> List[ExpUva]:
    return get_by_field(ano, ExpUva.ano, ExpUva, session)


@router.post("/criar_vinho/")
def create_vinho(vinho: ExpVinhos, session=Depends(get_session)):
    return create_item(vinho, ExpVinhos, session)


@router.patch("/atualizar_vinho/")
def update_vinho(vinho: ExpVinhos, session=Depends(get_session)) -> ExpVinhos:
    return update_item(vinho, ExpVinhos, session)


@router.get("/obter_vinho/{item_id}")
def get_vinho(item_id: int, session=Depends(get_session)) -> ExpVinhos:
    return get_item(item_id, ExpVinhos, session)


@router.delete("/excluir_vinho/{item_id}")
def delete_vinho(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ExpVinhos, session)


@router.get("/vinho_por_ano/{ano}")
def get_vinho_por_ano(ano: str, session=Depends(get_session)) -> List[ExpVinhos]:
    return get_by_field(ano, ExpVinhos.ano, ExpVinhos, session)
