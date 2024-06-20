from sqlalchemy import insert, text
from src.database import (
    async_engine,
    async_session_factory,
    session_factory,
    sync_engine,
    Base,
)
from src.models import (
    ExampleTable,
    ExampleTypes,
    metadata_obj,
    my_table,
    _ExampleEnumDecl,
    _ExampleEnumImp,
)


async def async_connect():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3"))
        print(f"{res.all()=}")


def create_tables():
    """Пересоздание всех объявленных таблиц"""
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


def insert_data():
    """Insert data"""
    stmt = insert(my_table).values(
        [
            {"first_col": "first_val", "enum_val": _ExampleEnumImp.first_var},
            {"first_col": None, "enum_val": "2"},
        ]
    )

    with sync_engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


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


async def async_insert_data_orm():
    async with async_session_factory() as session:
        first_data_obj = ExampleTable(first_col="first_val_orm_async")
        second_data_obj = ExampleTable(first_col="second_val_orm_async")

        session.add_all(
            [
                first_data_obj,
                second_data_obj,
            ]
        )

        await session.commit()


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

        session.add_all([data1, data2])

        session.commit()
