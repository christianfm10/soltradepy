from typing import TypeVar

from sqlmodel import Session

T = TypeVar("T")


class BaseRepository[T]:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
