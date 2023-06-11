__all__ = [
    "Base",
    "User",
]

from sqlalchemy import Column, String, text, UUID
from sqlalchemy.orm import declarative_base
from typing import Type

Base: Type = declarative_base()


class User(Base):
    __tablename__ = "users"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
