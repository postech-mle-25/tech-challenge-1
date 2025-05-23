from app.model.base_queries import create_item, delete_item, get_by_field, get_item, update_item
from typing import Type
from sqlmodel import SQLModel, Session

class BaseRouters:

    @staticmethod
    def create(model: SQLModel, route: Type[SQLModel], session: Session):
        return create_item(model, route, session)

    @staticmethod
    def get(item_id: int, route: Type[SQLModel], session: Session):
        return get_item(item_id, route, session)

    @staticmethod
    def update(model: SQLModel, route: Type[SQLModel], session: Session):
        return update_item(model, route, session)

    @staticmethod
    def delete(item_id: int, route: Type[SQLModel], session: Session):
        return get_item(item_id, route, session)

    @staticmethod
    def get_by_field(query: str, field, route: Type[SQLModel], session: Session):
        return get_by_field(query, field, route, session)
