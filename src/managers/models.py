from database_models.car_model import ModelCarModel
from config.manage_session import manage_connection


from schemas.models import CreateModelSchema, UpdateModelSchema
from sqlalchemy.orm import joinedload
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
        brand_name = filters.pop("brand_name", None)
        avg_price_min = filters.pop("avg_price_min", None)
        avg_price_max = filters.pop("avg_price_max", None)
        try:
            query = self.connection.query(ModelCarModel).options(
                joinedload(ModelCarModel.brand)
            )
            if brand_id:
                query = query.filter(ModelCarModel.brand_id == brand_id)
            if brand_name:
                query = query.filter(ModelCarModel.name == brand_name)
            if avg_price_min:
                query = query.filter(ModelCarModel.average_price >= avg_price_min)
            if avg_price_max:
                query = query.filter(ModelCarModel.average_price <= avg_price_max)

            logger.success("ModelsManager | get_models(): FINISHED")
            return query.all()
        except Exception as e:
            logger.error(f"ModelsManager | get_models(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def insert_new_model(self, model_data: CreateModelSchema):
        """Method to insert a new register in model table."""
        logger.info("ModelsManager | insert_new_model(): STARTED...")
        try:
            model = ModelCarModel(
                name=model_data.name,
                average_price=model_data.average_price,
                brand_id=model_data.brand_id,
            )
            self.connection.add(model)
            self.connection.commit()
            self.connection.refresh(model)
            logger.success("ModelsManager | insert_new_model(): FINISHED")
            return [model]
        except Exception as e:
            self.connection.rollback()
            logger.error(f"ModelsManager | insert_new_model(): ERROR - {e}")
            self.connection.close()
            return []

    @manage_connection
    def update_model(self, model_data: UpdateModelSchema):
        """Method to update a register in model table."""
        logger.info("ModelsManager | update_model(): STARTED...")
        try:
            clean_data = {"average_price": model_data.average_price}
            result = (
                self.connection.query(ModelCarModel)
                .filter(ModelCarModel.name == model_data.name)
                .update(clean_data, synchronize_session=False)
            )
            self.connection.commit()
            if result == 0:
                logger.warning(
                    "ModelsManager | update_model() - No model was updated (possibly invalid ID)."
                )
                return {"error": f"Model {model_data.name} was not updated"}

            filters = {"brand_name": model_data.name}
            result = self.get_models(**filters)
            logger.success("ModelsManager | update_model(): FINISHED")
            return result
        except Exception as e:
            self.connection.rollback()
            logger.error(f"ModelsManager | update_model(): ERROR - {e}")
            self.connection.close()
            return []


models_manager = ModelsManager()
