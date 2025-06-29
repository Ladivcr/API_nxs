from database_models.brand_model import BrandModel
from database_models.car_model import ModelCarModel
from config.manage_session import manage_connection
from sqlalchemy import select
from pudb import set_trace
from sqlalchemy.orm import joinedload # O selectinload
from config.settings import logger

class BrandManager:
    """Class to struct responses from database."""

    def __init__(self, connection: object = None):
        self.connection = connection
        
    @manage_connection
    def get_brands(self, **filters):
        """Method to request register from table brands in database."""
        logger.info("BrandManager | get_brands(): STARTED...")

        brand_name = filters.pop("brand_name", None)
        try:
            set_trace()
            query  = self.connection.query(BrandModel)
            if brand_name: 
                query = query.filter(BrandModel.name == brand_name)
            logger.success("BrandManager | get_brands(): FINISHED")
            return query.all()
        except Exception as e: 
            logger.error(f"BrandManager | get_brands(): ERROR - {e}")
            self.connection.close()
            return []

brand_manager = BrandManager()