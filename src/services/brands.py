from managers.brands import brand_manager
from managers.models import models_manager
from decimal import Decimal, ROUND_HALF_UP
from pudb import set_trace
class BranService:
    """Class to struct responses from database."""

    def _struct_response(self, data):
        """Method to struct the data."""

        response_list = []
        for item in data: 
            response_info={}
            filter = {"brand_id": item.id}
            info_linked_brand = models_manager.get_models(**filter)
            if len(info_linked_brand) > 0:
                response_info["id_brand"] = item.id 
                response_info["nombre"] = item.name
                prices = [obj.average_price for obj in info_linked_brand]
                avg_price = sum(prices) / len(prices)
                avg_price = avg_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                response_info["average_price"] = avg_price
                
                response_list.append(response_info)

        return response_list

    def list_brands(self, brand_name: str = None):
        """Method to control response from request SELECT in database."""
        filters = {"brand_name": brand_name}
        set_trace()
        response = brand_manager.get_brands(**filters)
        set_trace()
        final_response = self._struct_response(data=response)
        set_trace()
        return final_response

brand_service = BranService()