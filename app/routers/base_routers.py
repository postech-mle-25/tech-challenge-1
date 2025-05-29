from app.model.base_queries import BaseQuery
from typing import Type
from sqlmodel import SQLModel, Session

class BaseRouters:

    @staticmethod
    def create(model: SQLModel, route: Type[SQLModel], session: Session):
        return BaseQuery.create_item(model, route, session)

    @staticmethod
    def get(item_id: int, route: Type[SQLModel], session: Session):
        return BaseQuery.get_item(item_id, route, session)

    @staticmethod
    def update(model: SQLModel, route: Type[SQLModel], session: Session):
        return BaseQuery.update_item(model, route, session)

    @staticmethod
    def delete(item_id: int, route: Type[SQLModel], session: Session):
        return BaseQuery.delete_item(item_id, route, session)

    @staticmethod
    def get_by_field(query: str|int, field, route: Type[SQLModel], session: Session):
        return BaseQuery.get_by_field(query, field, route, session)

    @staticmethod
    def filter_by_period(before: int, after: int, field, route: Type[SQLModel], session: Session):
        return BaseQuery.filter_by_period(before, after, field, route, session)
