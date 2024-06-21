from sqlalchemy import text
from src.database import (
    async_engine,
    async_session_factory,
)
from src.models import (
    ExampleTable,
)


async def async_connect():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3"))
        print(f"{res.all()=}")


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
