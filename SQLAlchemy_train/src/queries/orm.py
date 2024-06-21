from sqlalchemy import select
from src.database import (
    session_factory,
    sync_engine,
    Base,
)
from src.models import (
    ExampleTable,
    ExampleTypes,
    _ExampleEnumDecl,
)


def create_tables_orm():
    """Пересоздание всех объявленных таблиц"""
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


def insert_data_orm():
    with session_factory() as session:
        first_data_obj = ExampleTable(first_col="first_val_orm")
        second_data_obj = ExampleTable(first_col="second_val_orm")

        session.add_all(
            [
                first_data_obj,
                second_data_obj,
            ]
        )

        session.commit()


def insert_data_orm__examples_types():
    with session_factory() as session:
        data1 = ExampleTypes(
            limit_val="non none value",
            maybe_none_val="not none value",
            enum_val=_ExampleEnumDecl.first_var,
            foreign_val=1,
        )
        data2 = ExampleTypes(
            limit_val="non none value",
            enum_val="2",
            foreign_val=2,
        )
        data3 = ExampleTypes(
            limit_val="value",
            enum_val="2",
            foreign_val=2,
        )

        session.add_all([data1, data2, data3])

        session.flush()
        session.commit()


def select_data_orm():
    with session_factory() as session:
        query = select(ExampleTypes)  # .filter_by(limit_val="non none value")
        result = session.execute(query)

        print(*result.all(), sep="\n")


def update_data_orm():
    with session_factory() as session:
        first_data_obj = session.get(ExampleTypes, {"id": 3})
        first_data_obj.maybe_none_val = "new_val"

        session.commit()
