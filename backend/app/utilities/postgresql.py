from typing import AsyncGenerator, Generator
from asyncio import current_task
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from app.utilities.config import CONFIG


# Synchronous - Read + Write
db_user = CONFIG.DB.USERNAME
db_pwd = CONFIG.DB.PASSWORD
db_host = CONFIG.DB.HOST
db_default_db = CONFIG.DB.DATABASE
db_port = CONFIG.DB.PORT
engine = create_engine(
    f"postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_default_db}",
    pool_recycle=300,
    pool_size=150,
    pool_use_lifo=True,
    pool_pre_ping=True,
    echo=True,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Asynchronous - Read + Write
async_engine = create_async_engine(
    f"postgresql+asyncpg://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_default_db}",
    pool_recycle=120,
    pool_size=150,
    pool_use_lifo=True,
    pool_pre_ping=True,
    echo=True,
    connect_args={"server_settings": {"jit": "off"}},
)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async_db_session = async_scoped_session(
        AsyncSessionLocal,
        scopefunc=current_task,
    )
    async with async_db_session() as db:
        yield db


# Synchronous - Read Only
slave_db_user = CONFIG.SLAVE_DB.USERNAME
slave_db_pwd = CONFIG.SLAVE_DB.PASSWORD
slave_db_host = CONFIG.SLAVE_DB.HOST
slave_db_default_db = CONFIG.SLAVE_DB.DATABASE
slave_db_port = CONFIG.SLAVE_DB.PORT
slave_engine = create_engine(
    # pylint: disable-next=line-too-long
    f"postgresql://{slave_db_user}:{slave_db_pwd}@{slave_db_host}:{slave_db_port}/{slave_db_default_db}",
    pool_recycle=120,
    pool_size=150,
    pool_use_lifo=True,
    pool_pre_ping=True,
    echo=True,
)
SlaveSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=slave_engine,
)


# Asynchronous - Read + Write
async_slave_engine = create_async_engine(
    f"postgresql+asyncpg://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_default_db}",
    pool_recycle=120,
    pool_size=150,
    pool_use_lifo=True,
    pool_pre_ping=True,
    echo=True,
    connect_args={"server_settings": {"jit": "off"}},
)
AsyncSlaveSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_slave_engine,
    class_=AsyncSession,
)


def get_slave_db() -> Generator[Session, None, None]:
    db = SlaveSessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_slave_db_context() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_slave_db() -> AsyncGenerator[AsyncSession, None]:
    async_db_session = async_scoped_session(
        AsyncSlaveSessionLocal,
        scopefunc=current_task,
    )
    db = async_db_session()
    try:
        yield db
    finally:
        if db.is_active:
            await db.close()
