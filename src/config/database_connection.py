from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from config.settings import logger, settings

@contextmanager
def open_connection_db():
    """Open and create a connection with database."""
    connection = create_engine(settings.DATABASE_URL)
    session_open = sessionmaker(bind=connection)
    Session = scoped_session(session_open)
    session_alive = Session()
    session_alive.expire_on_commit = False
    try: 
        logger.success("Connection: Open.")
        yield session_alive
        session_alive.commit()
    except Exception as e: 
        session_alive.rollback()
        raise e
    finally:
        logger.info("Connection: Closed.")
        session_alive.expunge_all()
        session_alive.close()