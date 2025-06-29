from database_models.car_model import ModelCarModel
from config.manage_session import manage_connection
from database_models.brand_model import BrandModel
from sqlalchemy import select
from pudb import set_trace
from sqlalchemy.orm import joinedload # O selectinload
from config.settings import logger

class ModelsManager:
    """Class to struct responses from database."""
    def __init__(self, connection: object = None):
        self.connection = connection
        
    @manage_connection
    def get_models(self, **filters):
        """Method to request register from table models in database."""
        logger.info("ModelsManager | get_models(): STARTED...")

        brand_id = filters.pop("brand_id", None)
        try: 
            query = self.connection.query(ModelCarModel).options(
                joinedload(ModelCarModel.brand)
            )
            if brand_id:
                query = query.filter(ModelCarModel.brand_id == brand_id)
            logger.success("ModelsManager | get_models(): FINISHED")
            return query.all()
        except Exception as e: 
            logger.error(f"ModelsManager | get_models(): ERROR - {e}")
            self.connection.close()
            return []

models_manager = ModelsManager()