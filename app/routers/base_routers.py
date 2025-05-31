from typing import Type, Any

from sqlmodel import SQLModel, Session

from app.model.base_queries import BaseQuery

class BaseRouters:

    @staticmethod
    def create(model: SQLModel, route: Type[SQLModel], session: Session) -> dict:
        return BaseQuery.create_item(model, route, session)

    @staticmethod
    def get(item_id: int, route: Type[SQLModel], session: Session) -> Type[SQLModel]:
        return BaseQuery.get_item(item_id, route, session)

    @staticmethod
    def update(model: SQLModel, route: Type[SQLModel], session: Session) -> Any:
        return BaseQuery.update_item(model, route, session)

    @staticmethod
    def delete(item_id: int, route: Type[SQLModel], session: Session) -> dict:
        return BaseQuery.delete_item(item_id, route, session)

    @staticmethod
    def get_by_field(query: str|int, field: str|int, route: Type[SQLModel], session: Session) -> Any:
        return BaseQuery.get_by_field(query, field, route, session)

    @staticmethod
    def filter_by_period(after: int, before: int, field: int, route: Type[SQLModel], session: Session) -> Any:
        return BaseQuery.filter_by_period(before, after, field, route, session)
