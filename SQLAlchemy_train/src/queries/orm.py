from pandas import read_sql
from sqlalchemy import Integer, and_, cast, func, select
from sqlalchemy.orm import contains_eager, joinedload, selectinload
from database import Base, session_factory, sync_engine
from models import (AnotherTestTable, ExampleTable, ExampleTypes,
                        LinkingTable, TestTable, Workload, _ExampleEnumDecl)


def get_data_for_insert(data: dict):
    return [
        dict((key, attr) for key, attr in zip(data, attrs))
        for attrs in zip(*data.values())
    ]


def create_tables_orm():
    """Пересоздание всех объявленных таблиц"""
    # sync_engine.echo = True
    Base.metadata.drop_all(sync_engine)
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
        data = dict(
            title=(
                "Python Junior Developer",
                "Python Developer",
                "Python Data Engineer",
                "Data Scientist",
            ),
            compensation=(50000, 150000, 250000, 300000),
            workload=(
                Workload.fulltime,
                Workload.fulltime,
                Workload.parttime,
                Workload.fulltime,
            ),
            worker_id=(1, 1, 2, 2),
        )

        session.add_all(TestTable(**kwargs) for kwargs in get_data_for_insert(data))
        session.commit()


def insert_link_data():
    with session_factory() as session:
        data1 = {
            "another_title": (
                "Programmer",
                "Manager",
                "Analyst",
                "Tester",
                "Boss",
                "Cleaner",
            ),
            "another_compensation": (100000, 70000, 150000, 90000, 1000000, 10000),
        }

        data2 = {
            "testtable_link": (2, 2, 3, 5, 6, 4, 1, 4, 5, 8, 9, 2),
            "anothertesttable_link": (1, 2, 4, 3, 3, 5, 1, 2, 6, 3, 4, 4),
            # "simple_text": (),
        }

        session.add_all(
            AnotherTestTable(**kwargs) for kwargs in get_data_for_insert(data1)
        )
        session.flush()
        session.add_all(LinkingTable(**kwargs) for kwargs in get_data_for_insert(data2))
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
        query = (
            select(ExampleTable)
            .options(joinedload(ExampleTable.extern_conn).joinedload(TestTable.to_anothertesttable))
            # .options(joinedload(TestTable.worker))
        )  # ВСЕ И ДАЖЕ ПУСТЫЕ

        # subq = (
        #     select(TestTable.id)
        #     .where(TestTable.worker_id == ExampleTable.id)
        #     .limit(1)
        #     .scalar_subquery()
        #     .correlate(ExampleTable)
        # )

        # query = (
        #     select(ExampleTable)
        #     .join(TestTable, TestTable.id.in_(subq))
        #     # .join(TestTable)
        #     .options(contains_eager(ExampleTable.extern_conn))
        # )  # ТОЛЬКО НЕ ПУСТЫЕ

        # result = session.execute(query)
        # result = result.unique().scalars().all()
        # print(*[item.extern_conn for item in result], sep="\n")

        df = read_sql(sql=query, con=session.connection())
        # df = df.drop(columns=["worker_id"])
        df.to_excel("output.xlsx")
        print(df)
