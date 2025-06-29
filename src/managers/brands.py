from database_models.brand_model import BrandModel

from config.manage_session import manage_connection

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
            query = self.connection.query(BrandModel)
            if brand_name:
                query = query.filter(BrandModel.name == brand_name)
            logger.success("BrandManager | get_brands(): FINISHED")
            return query.all()
        except Exception as e:
            logger.error(f"BrandManager | get_brands(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def insert_new_brand(self, brand_name: str):
        """Method to insert a new register in brand table."""
        logger.info("BrandManager | insert_new_brand(): STARTED...")
        try:
            brand = BrandModel(name=brand_name)
            self.connection.add(brand)
            self.connection.commit()
            self.connection.refresh(brand)
            logger.success("BrandManager | insert_new_brand(): FINISHED")
            return [brand]
        except Exception as e:
            self.connection.rollback()
            logger.error(f"BrandManager | get_brands(): ERROR - {e}")
            self.connection.close()
            return []


brand_manager = BrandManager()
