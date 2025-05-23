from typing import List

from app.auth import get_current_user
from app.db import get_session
from fastapi import APIRouter, Depends
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
def create(exporta: Exporta, session: Session = Depends(get_session)):
    return BaseRouters.create(exporta, Exporta, session)

@router.patch("/atualizar/")
def update(exporta: Exporta, session=Depends(get_session)) -> Exporta:
    return BaseRouters.update(exporta, Exporta, session)

@router.get("/obter/{item_id}")
def get(item_id: int, session=Depends(get_session)) -> Exporta:
    return BaseRouters.get(item_id, Exporta, session)

@router.delete("/excluir/{item_id}")
def delete(item_id: int, session=Depends(get_session)):
    return BaseRouters.delete(item_id, Exporta, session)

@router.get("/exporta/{ano}")
def get_by_year(year: str, session=Depends(get_session)) -> List[Exporta]:
    return BaseRouters.get_by_field(year, Exporta.ano, Exporta, session)
