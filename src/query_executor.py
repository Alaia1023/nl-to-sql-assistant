import sqlite3
import time

from src.database import DATABASE_PATH
from src.sql_safety import validate_read_only_sql


QUERY_TIMEOUT_SECONDS = 5
MAX_RESULT_ROWS = 100


def execute_sql(sql):
    validate_read_only_sql(sql)

    database_uri = f"file:{DATABASE_PATH.as_posix()}?mode=ro"

    connection = sqlite3.connect(
        database_uri,
        uri=True,
        timeout=QUERY_TIMEOUT_SECONDS,
    )

    try:
        connection.execute("PRAGMA query_only = ON")

        deadline = time.monotonic() + QUERY_TIMEOUT_SECONDS

        connection.set_progress_handler(
            lambda: int(time.monotonic() > deadline),
            1000,
        )

        cursor = connection.execute(sql)

        columns = [
            description[0]
            for description in cursor.description
        ]

        rows = cursor.fetchmany(MAX_RESULT_ROWS + 1)

        truncated = len(rows) > MAX_RESULT_ROWS
        rows = rows[:MAX_RESULT_ROWS]

        return {
            "columns": columns,
            "rows": [tuple(row) for row in rows],
            "truncated": truncated,
        }

    finally:
        connection.close()
