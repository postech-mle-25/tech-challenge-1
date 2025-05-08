from typing import List

# from .dependencies import get_token_header
from db import get_session
from fastapi import APIRouter, Depends
from model.base_queries import create_item, delete_item, filter_by_period, get_by_field, get_item, update_item
from model.processamento import *

router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar_mesa/")
def create_mesa(mesa: ProcessaMesa, session=Depends(get_session)):
    return create_item(mesa, ProcessaMesa, session)


@router.patch("/atualizar_mesa/")
def update_mesa(mesa: ProcessaMesa, session=Depends(get_session)) -> ProcessaMesa:
    return update_item(mesa, ProcessaMesa, session)


@router.get("/obter_mesa/{item_id}")
def get_mesa(item_id: int, session=Depends(get_session)) -> ProcessaMesa:
    return get_item(item_id, ProcessaMesa, session)


@router.delete("/excluir_mesa/{item_id}")
def delete_mesa(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ProcessaMesa, session)


@router.get("/mesa_por_ano/{ano}")
def get_mesa_por_ano(ano: int, session=Depends(get_session)) -> List[ProcessaMesa]:
    return get_by_field(ano, ProcessaMesa.ano, ProcessaMesa, session)


@router.get("/mesa_por_periodo/")
def get_mesa_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[ProcessaMesa]:
    return filter_by_period(ate, apos, ProcessaMesa.ano, ProcessaMesa, session)


@router.post("/criar_americana/")
def create_americana(americana: ProcessaAmericanas, session=Depends(get_session)):
    return create_item(americana, ProcessaAmericanas, session)


@router.patch("/atualizar_americana/")
def update_americana(
    americana: ProcessaAmericanas, session=Depends(get_session)
) -> ProcessaAmericanas:
    return update_item(americana, ProcessaAmericanas, session)


@router.get("/obter_americana/{item_id}")
def get_americana(item_id: int, session=Depends(get_session)) -> ProcessaAmericanas:
    return get_item(item_id, ProcessaAmericanas, session)


@router.delete("/excluir_americana/{item_id}")
def delete_americana(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ProcessaAmericanas, session)


@router.get("/americanas_por_ano/{ano}")
def get_americanas_por_ano(
    ano: int, session=Depends(get_session)
) -> List[ProcessaAmericanas]:
    return get_by_field(ano, ProcessaAmericanas.ano, ProcessaAmericanas, session)


@router.get("/americanas_por_periodo/")
def get_americanas_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[ProcessaAmericanas]:
    return filter_by_period(
        ate, apos, ProcessaAmericanas.ano, ProcessaAmericanas, session
    )


@router.post("/criar_vinifera/")
def create_vinifera(vinifera: ProcessaViniferas, session=Depends(get_session)):
    return create_item(vinifera, ProcessaViniferas, session)


@router.patch("/atualizar_vinifera/")
def update_vinifera(
    vinifera: ProcessaViniferas, session=Depends(get_session)
) -> ProcessaViniferas:
    return update_item(vinifera, ProcessaViniferas, session)


@router.get("/obter_vinifera/{item_id}")
def get_vinifera(item_id: int, session=Depends(get_session)) -> ProcessaViniferas:
    return get_item(item_id, ProcessaViniferas, session)


@router.delete("/excluir_vinifera/{item_id}")
def delete_vinifera(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ProcessaViniferas, session)


@router.get("/viniferas_por_ano/{ano}")
def get_viniferas_por_ano(
    ano: int, session=Depends(get_session)
) -> List[ProcessaViniferas]:
    return get_by_field(ano, ProcessaViniferas.ano, ProcessaViniferas, session)


@router.get("/viniferas_por_periodo/")
def get_viniferas_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[ProcessaViniferas]:
    return filter_by_period(
        ate, apos, ProcessaViniferas.ano, ProcessaViniferas, session
    )


@router.post("/criar_sem_class/")
def create_sem_class(sem_class: ProcessaSemclass, session=Depends(get_session)):
    return create_item(sem_class, ProcessaSemclass, session)


@router.patch("/atualizar_sem_class/")
def update_sem_class(
    sem_class: ProcessaSemclass, session=Depends(get_session)
) -> ProcessaSemclass:
    return update_item(sem_class, ProcessaSemclass, session)


@router.get("/obter_sem_class/{item_id}")
def get_sem_class(item_id: int, session=Depends(get_session)) -> ProcessaSemclass:
    return get_item(item_id, ProcessaSemclass, session)


@router.delete("/excluir_sem_class/{item_id}")
def delete_sem_class(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, ProcessaSemclass, session)


@router.get("/sem_class_por_ano/{ano}")
def get_sem_class_por_ano(
    ano: int, session=Depends(get_session)
) -> List[ProcessaSemclass]:
    return get_by_field(ano, ProcessaSemclass.ano, ProcessaSemclass, session)


@router.get("/sem_class_por_periodo/")
def get_sem_class_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[ProcessaSemclass]:
    return filter_by_period(ate, apos, ProcessaSemclass.ano, ProcessaSemclass, session)
