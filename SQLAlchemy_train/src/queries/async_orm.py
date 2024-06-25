from sqlalchemy import Integer, func, insert, select, text
from sqlalchemy.orm import aliased
from src.database import async_engine, async_session_factory
from src.models import ExampleTable, TestTable


async def async_connect():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3"))
        print(f"{res.all()=}")


async def async_insert_data_orm():
    async with async_session_factory() as session:
        first_data_obj = ExampleTable(first_col="Alasar")
        second_data_obj = ExampleTable(first_col="Bugomi")
        third_data_obj = ExampleTable(first_col="Joime")

        session.add_all([first_data_obj, second_data_obj, third_data_obj])

        await session.commit()


async def async_insert_test_data():
    async with async_session_factory() as session:
        testdata1 = [
            {"first_col": "Tromen"},
            {"first_col": "Bore"},
            {"first_col": "Adis"},
        ]
        testdata2 = [
            {
                "title": "Python Programmer",
                "compensation": 60000,
                "workload": "fulltime",
                "worker_id": 3,
            },
            {
                "title": "Python Learning Engineer",
                "compensation": 70000,
                "workload": "parttime",
                "worker_id": 3,
            },
            {
                "title": "Python Data Scientist",
                "compensation": 80000,
                "workload": "parttime",
                "worker_id": 4,
            },
            {
                "title": "Python Analyst",
                "compensation": 90000,
                "workload": "fulltime",
                "worker_id": 4,
            },
            {
                "title": "Python Junior Developer ",
                "compensation": 100000,
                "workload": "fulltime",
                "worker_id": 5,
            },
        ]

        await session.execute(insert(ExampleTable).values(testdata1))
        await session.execute(insert(TestTable).values(testdata2))

        await session.commit()


async def async_superjoin_data():
    """
    WITH test2 AS (
        SELECT *, compensation - avg_workload_compensation AS compensation_diff
        FROM
        (SELECT
            w.id,
            w.first_col,
            r.compensation,
            r.workload,
            avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
        FROM testtable r
        JOIN tablename w ON r.worker_id = w.id) test1
    )
    SELECT * FROM test2
    ORDER BY compensation_diff DESC
    """

    w = aliased(ExampleTable)
    r = aliased(TestTable)

    subq = (
        select(
            r,
            w,
            func.avg(r.compensation)
            .over(partition_by=r.workload)
            .cast(Integer)
            .label("avg_workload_compensation"),
        )
        .join(r, r.worker_id == w.id)
        .subquery("test1")
    )
    cte = select(
        subq.c.worker_id,
        subq.c.first_col,
        subq.c.compensation,
        subq.c.workload,
        subq.c.avg_workload_compensation,
        (subq.c.compensation - subq.c.avg_workload_compensation).label(
            "compensation_diff"
        ),
    ).cte("test2")
    query = select(cte).order_by(cte.c.compensation_diff.desc())

    async with async_session_factory() as session:
        res = await session.execute(query)

        print(*res.all(), sep="\n")
