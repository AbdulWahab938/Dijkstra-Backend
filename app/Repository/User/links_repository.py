from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from Schema.SQL.Models.models import Links

class LinksRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, link: Links) -> Links:
        try:
            self.session.add(link)
            self.session.commit()
            self.session.refresh(link)
            return link
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get(self, link_id: UUID) -> Optional[Links]:
        statement = select(Links).where(Links.id == link_id)
        return self.session.exec(statement).first()

    def get_by_user_id(self, user_id: UUID) -> Optional[Links]:
        statement = select(Links).where(Links.user_id == user_id)
        return self.session.exec(statement).first()

    def list(self, skip: int = 0, limit: int = 20) -> List[Links]:
        statement = select(Links).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, link: Links) -> Links:
        try:
            self.session.add(link)
            self.session.commit()
            self.session.refresh(link)
            return link
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def delete(self, link: Links) -> None:
        try:
            self.session.delete(link)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
