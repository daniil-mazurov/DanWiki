from sqlalchemy import Integer, and_, cast, func, select
from src.database import Base, session_factory, sync_engine
from src.models import ExampleTable, ExampleTypes, TestTable, Workload, _ExampleEnumDecl
from sqlalchemy.orm import joinedload, selectinload

from pandas import read_sql


def create_tables_orm():
    """Пересоздание всех объявленных таблиц"""
    Base.metadata.drop_all(sync_engine)
    # sync_engine.echo = True
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = False


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


def insert_test_data():
    with session_factory() as session:
        data1 = TestTable(
            title="Python Junior Developer",
            compensation=50000,
            workload=Workload.fulltime,
            worker_id=1,
        )
        data2 = TestTable(
            title="Python Developer",
            compensation=150000,
            workload=Workload.fulltime,
            worker_id=1,
        )
        data3 = TestTable(
            title="Python Data Engineer",
            compensation=250000,
            workload=Workload.parttime,
            worker_id=2,
        )
        data4 = TestTable(
            title="Data Scientist",
            compensation=300000,
            workload=Workload.fulltime,
            worker_id=2,
        )

        session.add_all([data1, data2, data3, data4])

        session.commit()


def select_data_orm():
    with session_factory() as session:
        query = select(ExampleTypes)  # .filter_by(limit_val="non none value")
        result = session.execute(query)

        print(*result.all(), sep="\n")


def select_test_data():
    # select workload, avg(compensation)::int as avg_compensation
    # from public.testtable
    # where title like '%Python%' and compensation > 40000
    # group by workload

    with session_factory() as session:
        query = (
            select(
                TestTable.workload,
                cast(func.avg(TestTable.compensation), Integer).label(
                    "avg_compensation"
                ),
            )
            .select_from(TestTable)
            .where(
                and_(
                    TestTable.title.contains("Python"),
                    TestTable.compensation > 40000,
                )
            )
            .group_by(TestTable.workload)
            # .having(cast(func.avg(TestTable.compensation), Integer) > 70000)
        )

        # print(query.compile(compile_kwargs={"literal_binds": True}))

        # result = session.execute(query)

        # print(result.all())

        df = read_sql(sql=query, con=session.connection())
        
        print(df)


def update_data_orm():
    with session_factory() as session:
        first_data_obj = session.get(ExampleTypes, {"id": 3})
        first_data_obj.maybe_none_val = "new_val"

        session.commit()


def joined_load_data():
    with session_factory() as session:
        query = select(ExampleTable).options(joinedload(ExampleTable.extern_conn))

        # result = session.execute(query)
        # result = result.unique().scalars().all()
        # print(*[item.extern_conn for item in result], sep="\n")
        
        df = read_sql(sql=query, con=session.connection())
        
        print(df)

