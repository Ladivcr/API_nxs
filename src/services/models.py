from managers.models import models_manager
from config.settings import logger
from schemas.models import CreateModelSchema, ModelSchema, UpdateModelSchema
from fastapi.responses import JSONResponse


class ModelService:
    """Class to struct responses from database."""

    def _struct_response(self, data):
        """Method to struct the data."""
        logger.info("ModelService | _struct_reponse(): STARTED...")
        list_response = []
        for item in data:
            tmp_dict = {
                "id_model": item.id,
                "name_model": item.name,
                "average_price": item.average_price,
            }
            list_response.append(tmp_dict)

        logger.success("ModelService | _struct_reponse(): FINISHED")
        return list_response

    def _control_data_type(self, data):
        """Method to control data types"""
        response_list = []
        for item in data:
            tmp = ModelSchema(
                id=item.id,
                name=item.name,
                average_price=item.average_price,
                brand_id=item.brand_id,
            )
            response_list.append(tmp.model_dump(exclude_none=True))

        return response_list

    def list_models(
        self,
        brand_id: int = None,
        struct_response: bool = True,
        max_avg_price: float = None,
        min_avg_price: float = None,
    ):
        """Method to control response from request SELECT in database."""
        logger.info("ModelService | list_models(): STARTED...")
        filters = {
            "brand_id": brand_id,
            "avg_price_max": max_avg_price,
            "avg_price_min": min_avg_price,
        }
        response = models_manager.get_models(**filters)
        if struct_response is True:
            response = self._struct_response(data=response)

        logger.success("ModelService | _struct_reponse(): FINISHED")
        return response

    def create_new_model(self, data_model: CreateModelSchema, brand_id: int):
        """Method to control flow during insert to db."""
        # Check if brand exist
        logger.info("ModelService | create_new_model(): STARTED...")
        data_model.brand_id = brand_id
        filters = {"brand_name": data_model.name}
        response = models_manager.get_models(**filters)
        if len(response) > 0:
            return JSONResponse(
                status_code=400,
                content={"error": f"Model '{data_model.name}' already exist!"},
            )

        response = models_manager.insert_new_model(model_data=data_model)
        logger.success("ModelService | create_new_model(): FINISHED")
        if len(response) > 0:
            response = self._control_data_type(data=response)
            logger.success("ModelService | list_brands(): FINISHED")
            return JSONResponse(status_code=201, content=response[0])
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"New Model '{data_model.name}' was not created!"},
            )

    def update_model(self, data: UpdateModelSchema):
        """Method to control flow during update."""
        logger.info("ModelService | update_model(): STARTED...")
        filters = {"brand_name": data.name}
        response = models_manager.get_models(**filters)
        if len(response) == 0:
            return JSONResponse(
                status_code=400, content={"error": f"Model '{data.name}' does not exist!"}
            )
        response = models_manager.update_model(model_data=data)

        if isinstance(response, dict):
            return response
        elif len(response) > 0:
            response = self._control_data_type(data=response)
            logger.success("ModelService | update_model(): FINISHED")
            return JSONResponse(status_code=201, content=response[0])
        return JSONResponse(
            status_code=400, content={"error": f"Model '{data.name}' was not updated!"}
        )


model_service = ModelService()
