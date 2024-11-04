import os
from contextlib import asynccontextmanager

import asyncpg
from asyncpg.exceptions import PostgresConnectionError
from fastapi import HTTPException


@asynccontextmanager
async def get_database_connection():
    conn = None
    try:
        conn = await asyncpg.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST')
        )
        yield conn
    except PostgresConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail='Ошибка подключения к базе данных') from e
    finally:
        if conn:
            await conn.close()