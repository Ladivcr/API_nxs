from config.manage_session import manage_connection
from config.settings import logger
from sqlalchemy import text

pass


class GeneralOperationsDB:
    """Class to manage all general direct operations to database."""

    def __init__(self, connection: object = None):
        self.connection = connection

    @manage_connection
    def ping_db(self) -> bool:
        try:
            result = self.connection.execute(text("SELECT 1")).scalar()
            if result == 1:
                logger.success("Ping OK.")
                return True
            else:
                logger.error("Ping Fail.")
                return False
        except Exception as e:
            logger.error(f"Ping failed due to exception: {e}")
            return False


general_operations_db = GeneralOperationsDB()
