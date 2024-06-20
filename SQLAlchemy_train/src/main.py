import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

import asyncio

from src.queries.core import *

create_tables()
insert_data()
create_tables_orm()
insert_data_orm()

# asyncio.run(async_insert_data_orm())

insert_data_orm__examples_types()