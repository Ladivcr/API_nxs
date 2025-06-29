from database_models.brand_model import BrandModel
from database_models.car_model import ModelCarModel
from services.models import model_service
from decimal import Decimal


class TestModelServiceConfig:
    obj_brand = BrandModel(id=1, name="Aston Martin")
    obj_model = ModelCarModel(
        id=1, name="Romero", average_price=Decimal(100000), brand_id=1
    )

    def test_struct_response_model_service(self):
        """Test struct response method."""
        response = model_service._struct_response(data=[self.obj_model])
        assert isinstance(response, list) is True
        assert len(response) == 1
        assert response[0]["name_model"] == "Romero"

    def test_control_response_model_service(self):
        """Test control response method."""
        response = model_service._control_data_type(data=[self.obj_model])
        assert isinstance(response, list) is True
        assert isinstance(response[0], dict) is True
        assert response[0]["name"] == "Romero"
