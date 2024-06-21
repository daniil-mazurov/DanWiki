import enum
from datetime import UTC, datetime
from typing import Annotated

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    DateTime,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


#
# Императивный стиль
#
class _ExampleEnumImp(enum.Enum):
    first_var = "1"
    second_var = "2"


metadata_obj = MetaData()
"""Метаданные о созданных таблицах"""


my_table = Table(
    "tablename_old",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("first_col", String(50)),
    Column(
        "enum_val",
        Enum(_ExampleEnumImp, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    ),
    Column("date_val", DateTime, server_default=func.now()),
)


#
# Декларативный стиль
#
class _ExampleEnumDecl(enum.Enum):
    first_var = "1"
    second_var = "2"


class ExampleTable(Base):
    __tablename__ = "tablename"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_col: Mapped[str]


intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]


class ExampleTypes(Base):
    __tablename__ = "types_examples"

    id: Mapped[intpk]
    limit_val: Mapped[str | None] = mapped_column(String(50))
    maybe_none_val: Mapped[str_256 | None]
    enum_val: Mapped[_ExampleEnumDecl] = mapped_column(
        Enum(_ExampleEnumDecl, values_callable=lambda obj: [e.value for e in obj])
    )
    foreign_val: Mapped[int | None] = mapped_column(
        ForeignKey(
            "tablename.id",
            ondelete="CASCADE",
            # ondelete="SET NULL",
        )
    )
    # foreign_val: Mapped[int] = mapped_column(ForeignKey(ExampleTable.id))
    date_val: Mapped[datetime] = mapped_column(server_default=func.now())
    # date_val: Mapped[datetime] = mapped_column(
    #     server_default=text("TIMEZONE('utc',now())")
    # )
    # date_val: Mapped[datetime] = mapped_column(default=datetime.now())
