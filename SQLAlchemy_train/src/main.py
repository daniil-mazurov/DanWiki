import os
import sys

# sys.path.insert(1, os.path.join(sys.path[0], ".."))
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# print(sys.path)

from src.queries.core import (
    create_tables,
    create_tables_orm,
    insert_data,
    insert_data_orm,
    async_insert_data_orm,
)
import asyncio


create_tables()
insert_data()
create_tables_orm()
insert_data_orm()

asyncio.run(async_insert_data_orm())
