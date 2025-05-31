from typing import List, Type, Any

from sqlmodel import SQLModel
from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.db import get_session
from app.model.tables import Exporta
from app.routers.base_routers import BaseRouters
from sqlmodel import Session


router = APIRouter(
    prefix="/exportacao",
    tags=["exportacao"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/criar/")
def create(exporta: Exporta, session: Session = Depends(get_session)) -> dict:
    return BaseRouters.create(exporta, Exporta, session)

@router.patch("/atualizar/")
def update(exporta: Exporta, session=Depends(get_session)) -> Exporta:
    return BaseRouters.update(exporta, Exporta, session)

@router.get("/obter/")
def get(item_id: int, session=Depends(get_session)) -> Exporta:
    return BaseRouters.get(item_id, Exporta, session)

@router.delete("/excluir/")
def delete(item_id: int, session=Depends(get_session)) -> dict:
    return BaseRouters.delete(item_id, Exporta, session)

@router.get("/exportacao_por_ano/")
def get_exportacao_por_ano(ano: str, session=Depends(get_session)) -> List[Exporta]:
    return BaseRouters.get_by_field(ano, Exporta.ano, Exporta, session)

@router.get("/exportacao_por_tipo/")
def get_exportacao_por_tipo(tipo: str, session=Depends(get_session)) -> List[Exporta]:
    return BaseRouters.get_by_field(tipo, Exporta.tipo, Exporta, session)