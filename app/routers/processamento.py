from typing import List

from app.auth import get_current_user
from app.db import get_session
from fastapi import APIRouter, Depends
from app.model.base_queries import create_item, delete_item, filter_by_period, get_by_field, get_item, update_item
from app.model.tables import Processamento

router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/criar/")
def create_proc(proc: Processamento, session=Depends(get_session)):
    return create_item(proc, Processamento, session)


@router.patch("/atualizar/")
def update_proc(proc: Processamento, session=Depends(get_session)) -> Processamento:
    return update_item(proc, Processamento, session)


@router.get("/obter/{item_id}")
def get_proc(item_id: int, session=Depends(get_session)) -> Processamento:
    return get_item(item_id, Processamento, session)


@router.delete("/excluir/{item_id}")
def delete_proc(item_id: int, session=Depends(get_session)):
    return delete_item(item_id, Processamento, session)


@router.get("/proc_por_ano/{ano}")
def get_proc_por_ano(ano: int, session=Depends(get_session)) -> List[Processamento]:
    return get_by_field(ano, Processamento.ano, Processamento, session)


@router.get("/proc_por_periodo/")
def get_proc_por_periodo(
    apos: int, ate: int, session=Depends(get_session)
) -> List[Processamento]:
    return filter_by_period(ate, apos, Processamento.ano, Processamento, session)


@router.get("/{tipo}")
def get_proc_por_tipo(tipo: str, session=Depends(get_session)) -> List[Processamento]:
    return get_by_field(tipo, Processamento.tipo, Processamento, session)
