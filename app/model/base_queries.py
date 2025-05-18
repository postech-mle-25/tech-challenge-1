from fastapi import HTTPException
from sqlmodel import select


def get_item(item_id, table, session):
    item = session.get(table, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


def create_item(item, table, session):
    db_item = table.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return {"id": db_item.id}


def update_item(item, table, session):
    item_db = session.get(table, item.id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    mesa_data = item.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(mesa_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db


def delete_item(item_id, table, session):
    item = session.get(table, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}


def get_by_field(q, field, table, session):
    statement = select(table).where(field == q)
    results = session.exec(statement)
    return results


def filter_by_period(before, after, field, table, session):
    statement = select(table).where(field >= after).where(field <= before)
    results = session.exec(statement)
    return results
