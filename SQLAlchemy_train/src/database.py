from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,  # Логирование всех выполняемых операций
    pool_size=5,  # Максимальное количество подключений к базе
    max_overflow=10,  # Количество дополнительных подключений при переполнении
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,  # Логирование всех выполняемых операций
    pool_size=5,  # Максимальное количество подключений к базе
    max_overflow=10,  # Количество дополнительных подключений при переполнении
)


session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
