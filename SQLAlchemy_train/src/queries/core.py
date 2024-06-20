from sqlalchemy import text, insert
from src.database import (
    sync_engine,
    async_engine,
    session_factory,
    async_session_factory,
)
from src.models import metadata_obj, my_table, ExampleTable


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
            {"first_col": "first_val"},
            {"first_col": "second_val"},
        ]
    )

    with sync_engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


def create_tables_orm():
    """Пересоздание всех объявленных таблиц"""
    sync_engine.echo = False
    ExampleTable.metadata.drop_all(sync_engine)
    ExampleTable.metadata.create_all(sync_engine)
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
