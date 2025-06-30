from managers.brands import brand_manager
from managers.models import models_manager
from decimal import Decimal, ROUND_HALF_UP
from config.settings import logger
from fastapi.responses import JSONResponse
from schemas.brands import BrandSchema


class BrandService:
    """Class to struct responses from database."""

    def _struct_response(self, data):
        """Method to struct the data."""
        logger.info("BrandService | _struct_response(): STARTED...")
        response_list = []
        for item in data:
            response_info = {}
            filter = {"brand_id": item.id}
            info_linked_brand = models_manager.get_models(**filter)
            if len(info_linked_brand) > 0:
                response_info["id_brand"] = item.id
                response_info["nombre"] = item.name
                prices = [obj.average_price for obj in info_linked_brand]
                avg_price = sum(prices) / len(prices)
                avg_price = avg_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                response_info["average_price"] = float(
                    avg_price.quantize(Decimal("0.01"))
                )

                response_list.append(response_info)

        logger.success("BrandService | _struct_response(): FINISHED")
        return response_list

    def _control_data_type(self, data):
        """Method to control data types"""
        response_list = []
        for item in data:
            tmp = BrandSchema(id=item.id, name=item.name)
            response_list.append(tmp.model_dump())
        return response_list

    def list_brands(self, brand_name: str = None, struct_response: bool = True):
        """Method to control response from request SELECT in database."""
        logger.info("BrandService | list_brands(): STARTED...")
        filters = {"brand_name": brand_name}
        response = brand_manager.get_brands(**filters)
        if len(response) > 0:
            if struct_response is True:
                response = self._struct_response(data=response)
            else:
                response = self._control_data_type(data=response)
            logger.success("BrandService | list_brands(): FINISHED")
            return JSONResponse(status_code=200, content=response)
        logger.success("BrandService | list_brands(): FINISHED")
        return JSONResponse(status_code=200, content=[])

    def create_new_brand(self, brand_name: str):
        """Method to control flow during insert to db."""
        # Check if brand exist
        logger.info("BrandService | create_new_brand(): STARTED...")
        filters = {"brand_name": brand_name}
        response = brand_manager.get_brands(**filters)
        if len(response) > 0:
            return JSONResponse(
                status_code=400, content={"error": f"Brand '{brand_name}' already exist!"}
            )

        response = brand_manager.insert_new_brand(brand_name=brand_name)
        logger.success("BrandService | create_new_brand(): FINISHED")
        if len(response) > 0:
            response = self._control_data_type(data=response)
            logger.success("BrandService | list_brands(): FINISHED")
            return JSONResponse(status_code=201, content=response[0])
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"New Brand '{brand_name}' was not created! Please retry..."
                },
            )


brand_service = BrandService()
