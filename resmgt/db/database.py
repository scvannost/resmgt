__all__ = [
    "Database",
    "load_dotenv_config",
]

from dotenv import dotenv_values
import logging
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from typing import Any, Dict, List, Type
from urllib.parse import quote_plus

from .models import *  # drop dot when running directly

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)


class Database:
    Session: Type = None
    engine: Engine = None
    session: Session = None
    host: str = "localhost"
    port: int = 5432

    @staticmethod
    def _generate_connection_string(
        user: str,
        password: str,
        database: str,
        host: str,
        port: int,
    ) -> str:
        return f"postgresql://{quote_plus(user)}:{quote_plus(password)}@{quote_plus(host)}:{port}/{quote_plus(database)}"

    def add(self, *args, **kwargs) -> None:
        self.session.add(*args, **kwargs)
        self.session.commit()

    def add_all(self, *args, **kwargs) -> None:
        self.session.add_all(*args, **kwargs)
        self.session.commit()

    def close_session(self) -> None:
        self.session.close()
        self.session = None

    def connect(
        self,
        user: str,
        password: str,
        database: str,
        host: str = "localhost",
        port: int = 5432,
        *,
        create_db_if_not_exist: bool = True,
    ) -> None:
        self.engine = create_engine(
            self._generate_connection_string(
                user=user, password=password, database=database, host=host, port=port
            )
        )
        self.Session = sessionmaker(bind=self.engine)

        if (
            not database_exists(
                self._generate_connection_string(
                    user=user,
                    password=password,
                    database=database,
                    host=host,
                    port=port,
                )
            )
            and create_db_if_not_exist
        ):
            create_database(
                self._generate_connection_string(
                    user=user,
                    password=password,
                    database=database,
                    host=host,
                    port=port,
                )
            )

    def create_all_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def delete(self, *args, **kwargs) -> None:
        self.session.delete(*args, **kwargs)
        self.session.commit()

    def disconnect(self, *, close_session_if_needed: bool = True) -> None:
        if close_session_if_needed and self.session is not None:
            self.close_session()
        self.engine.dispose()
        self.engine = None

    def drop_all_tables(self, *, close_session_if_needed: bool = True) -> None:
        if close_session_if_needed and self.session is not None:
            self.close_session()

        ordered_tables: List[Type] = [
            VillagerTasks,
            Villager,
            Building,
            # BuildingType,
            User,
        ]

        for tbl in ordered_tables:
            tbl.__table__.drop(self.engine)

    def drop_database(
        self,
        user: str,
        password: str,
        database: str,
        host: str = "localhost",
        port: int = 5432,
        *,
        close_session_if_needed: bool = True,
    ) -> None:
        if close_session_if_needed and self.session is not None:
            self.close_session()
        drop_database(
            self._generate_connection_string(
                user=user, password=password, database=database, host=host, port=port
            )
        )

    def execute(self, *args, **kwargs) -> Any:
        return self.session.execute(*args, **kwargs)

    def merge(self, *args, **kwargs) -> Any:
        return self.session.merge(*args, **kwargs)

    def open_session(self) -> None:
        if self.Session is not None:
            self.session = self.Session()
        else:
            raise RuntimeError("You must call init_db() before get_session()")


def load_dotenv_config() -> Dict[str, Any]:
    config: Dict = dotenv_values()

    all_kwargs: Dict = {
        "host": config.get("PGHOST"),
        "port": config.get("PGPORT"),
        "database": config.get("PGDATABASE"),
        "user": config.get("PGUSER"),
        "password": config.get("PGPASSWORD"),
    }
    return {k: v for k, v in all_kwargs.items() if v is not None}
