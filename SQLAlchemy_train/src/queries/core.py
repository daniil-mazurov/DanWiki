from sqlalchemy import insert, select, text, update
from src.database import sync_engine
from src.models import _ExampleEnumImp, metadata_obj, my_table


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
            {
                "first_col": "first_val",
                "enum_val": _ExampleEnumImp.first_var,
            },
            {
                "first_col": None,
                "enum_val": "2",
            },
        ]
    )

    with sync_engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


def select_data():
    query = select(my_table)  # SELECT * FROM tablename

    with sync_engine.connect() as conn:
        result = conn.execute(query)

        print(*result.all(), sep="\n")


def update_data():
    id = 2
    new_value = "second_val"

    # stmt = text("UPDATE tablename_old SET first_col=:new_value WHERE id=:id")
    # stmt = stmt.bindparams(id=id, new_value=new_value)

    stmt = update(my_table).values(first_col=new_value).filter_by(id=id)

    with sync_engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
