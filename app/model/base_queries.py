from typing import Type, Any

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel import SQLModel, Session

class BaseQuery:

    @staticmethod
    def get_item(item_id: int, table: Type[SQLModel], session: Session) -> Type[SQLModel]:
        item = session.get(table, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @staticmethod
    def create_item(item: SQLModel, table: Type[SQLModel], session: Session) -> dict:
        db_item = table.model_validate(item)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return {"id": db_item.id}

    @staticmethod
    def update_item(item: SQLModel, table: Any, session: Session) -> Any:
        item_db = session.get(table, item.id)
        if not item_db:
            raise HTTPException(status_code=404, detail="Item not found")
        mesa_data = item.model_dump(exclude_unset=True)
        item_db.sqlmodel_update(mesa_data)
        session.add(item_db)
        session.commit()
        session.refresh(item_db)
        return item_db

    @staticmethod
    def delete_item(item_id: int, table: Type[SQLModel], session: Session) -> dict:
        item = session.get(table, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"ok": True}

    @staticmethod
    def get_by_field(q: str|int, field: str|int, table: Type[SQLModel], session: Any) -> Any:
        statement = select(table).where(field == q)
        results = session.exec(statement)
        return results

    @staticmethod
    def filter_by_period(after: int, before: int, field: int, table: Type[SQLModel], session: Any) -> Any:
        statement = select(table).where(field >= after).where(field <= before)
        results = session.exec(statement)
        return results
