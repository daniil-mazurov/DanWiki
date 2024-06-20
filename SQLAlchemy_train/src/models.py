from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
# import enum

#
# Императивный стиль
#

metadata_obj = MetaData()
"""Метаданные о созданных таблицах"""


my_table = Table(
    "tablename",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("first_col", String),
)


#
# Декларативный стиль
#


# class _ExampleEnum(enum.Enum):
#     first_var = 'first_val'
#     second_var = 'second_val'



class ExampleTable(Base):
    __tablename__ = "tablename"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_val = Mapped[str]
    

# class ExampleTypes(Base):
#     __tablename__ = 'types_examples'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     not_none_val: Mapped[str]
#     maybe_none_val: Mapped[int | None]
#     enum_val: Mapped[_ExampleEnum]
    