import logging
import os
from typing import Any
from typing import Iterable
from typing import Optional

import psycopg2

logger = logging.getLogger(__name__)

class Session:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def execute(self, sql: str, values: Optional[Iterable[Any]] = None) -> None:
        self._cursor.execute(sql, values)

    def commit(self):
        self._connection.commit()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exception_type, exception_value, trace):
        # Exit is transactional, in case of any exception - transaction will be rolled back
        if exception_type is not None:
            self._connection.rollback()
            logger.error(f"DB exception: {exception_value}")
        self._connection.close()
        self._cursor.close()

    def _connect(self) -> None:
        self._connection = psycopg2.connect(
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST', 'db'),
            port=os.getenv('POSTGRES_PORT', 5432),
        )
        self._cursor = self._connection.cursor()
