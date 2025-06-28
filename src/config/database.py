from functools import wraps

import psycopg2

from config.settings import logger, settings

DB_URL = settings.DATABASE_URL


def open_db_connection(func):
    """Decorator to manage database connection."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(DB_URL)
            conn.autocommit = True
            cursor = conn.cursor()
            return func(*args, cursor, **kwargs)

        except Exception as e:
            logger.exception(f"Error when trying to connect to db: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
                logger.info("Cursor: Closed.")
            if conn:
                conn.close()
                logger.info("Connection: Closed.")

    return wrapper
