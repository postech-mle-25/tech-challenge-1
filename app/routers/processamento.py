from fastapi import APIRouter, Depends, HTTPException

from model.processamento import *
# from .dependencies import get_token_header
from db import get_session

router = APIRouter(

    prefix="/processamento",
    tags=["processamento"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# session = get_session()


def get_proc(item_id, table, session):
    item = session.get(table, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def create_proc(item, table, session):
    db_item = table.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return {"id": db_item.id}

def update_proc(item, table, session):
    item_db = session.get(table, item.id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    mesa_data = item.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(mesa_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db

def delete_proc(item_id, table, session):
    item = session.get(table, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}


@router.post("/criar_mesa/")
def create_mesa(mesa: ProcessaMesa, session = Depends(get_session)):
    return create_proc(mesa, ProcessaMesa, session)

@router.patch("/atualizar_mesa/")
def update_mesa(mesa: ProcessaMesa, session = Depends(get_session)) -> ProcessaMesa:
    return update_proc(mesa, ProcessaMesa, session)

@router.get("/obter_mesa/{item_id}")
def get_mesa(item_id: int, session = Depends(get_session)) -> ProcessaMesa:
    return get_proc(item_id, ProcessaMesa, session)

@router.delete("/excluir_mesa/{item_id}")
def delete_mesa(item_id: int, session = Depends(get_session)):
    return delete_proc(item_id, ProcessaMesa, session)



