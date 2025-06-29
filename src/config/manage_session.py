from config.database_connection import open_connection_db


def manage_connection(method):
    """Decorator to use connection."""

    def wrapper(self, *args, **kwargs):
        with open_connection_db() as connection:
            self.connection = connection
            return method(self, *args, **kwargs)

    return wrapper
