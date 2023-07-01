__all__ = [
    "Base",
    "Building",
    "BuildingType",
    "User",
    "Villager",
    "VillagerTask",
]

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Any, Dict, Optional, Set
from uuid import UUID


# declarative base class
class Base(DeclarativeBase):
    def __str__(self) -> str:
        ret: Dict[str, Any] = dict()
        for key in dir(self):
            if not key.startswith("_") and key not in ["metadata", "registry"]:
                value: Any = getattr(self, key)
                ret[key] = value
        return str(ret)


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    residents: Mapped[Set["Villager"]] = relationship(
        foreign_keys="Villager.house_id", back_populates="house"
    )
    workers: Mapped[Set["Villager"]] = relationship(
        foreign_keys="Villager.work_id", back_populates="work"
    )


class BuildingType(Base):
    __tablename__ = "building_types"
    name: Mapped[str] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"
    uuid: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


class Villager(Base):
    __tablename__ = "villagers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    x: Mapped[float] = mapped_column(default=0.0)
    y: Mapped[float] = mapped_column(default=0.0)
    hunger: Mapped[float] = mapped_column(default=0.0)
    tiredness: Mapped[float] = mapped_column(default=0.0)
    happiness: Mapped[float] = mapped_column(default=0.0)
    healthiness: Mapped[float] = mapped_column(default=0.0)
    house_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Building.id))
    work_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Building.id))
    house: Mapped[Optional[Building]] = relationship(
        foreign_keys=house_id, back_populates="residents"
    )
    work: Mapped[Optional[Building]] = relationship(
        foreign_keys=work_id, back_populates="workers"
    )
    task_queue: Mapped[Set["VillagerTask"]] = relationship(back_populates="villager")


class VillagerTask(Base):
    __tablename__ = "villager_tasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    villager_id: Mapped[int] = mapped_column(
        ForeignKey(Villager.id, ondelete="cascade")
    )
    villager: Mapped[Villager] = relationship(back_populates="task_queue")
