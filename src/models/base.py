import time
from abc import abstractmethod
from typing import Annotated, Final, TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy import (
    text,
    UUID,
)
from sqlalchemy.orm import (
    mapped_column,
    DeclarativeBase,
    declared_attr,
)

Schema = TypeVar("Schema", bound=BaseModel)
SELECTIN: Final[str] = "selectin"
JOINED: Final[str] = "joined"


class BaseModelORM(DeclarativeBase, Generic[Schema]):
    __abstract__ = True
    repr_cols_num = 3
    repr_cols = tuple()

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()[:-3]}"

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    @abstractmethod
    def to_read_model(self) -> Schema: ...


timeSeconds = Annotated[
    int,
    mapped_column(
        server_default=text("extract(epoch FROM now())"),
        nullable=False,
    ),
]
timeSecondsOnUpdate = Annotated[
    int,
    mapped_column(
        server_default=text("extract(epoch FROM now())"),
        onupdate=int(time.time()),
        nullable=False,
    ),
]
boolFalse = Annotated[bool, mapped_column(default=False, nullable=False)]
boolTrue = Annotated[bool, mapped_column(default=True, nullable=False)]
uuid_pk = Annotated[
    UUID,
    mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid7()")),
]
uuid_type = Annotated[UUID, mapped_column(UUID(as_uuid=True))]
