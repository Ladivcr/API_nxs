from config.database import open_db_connection
from config.settings import logger

pass


class GeneralOperationsDB:
    """Class to manage all general direct operations to database."""

    @open_db_connection
    def ping_db(self, cursor) -> bool:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        if result and result[0] == 1:
            logger.success("Ping OK.")
            return True
        else:
            logger.error("Ping Fail.")
            return False


general_operations_db = GeneralOperationsDB()
