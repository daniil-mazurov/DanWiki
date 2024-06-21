import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

import asyncio

from src.queries.core import *
from src.queries.orm import *
from src.queries.async_orm import *

# create_tables()
# insert_data()
# select_data()
# update_data()

create_tables_orm()
insert_data_orm()
insert_data_orm__examples_types()
select_data_orm()
update_data_orm()


# asyncio.run(async_insert_data_orm())
