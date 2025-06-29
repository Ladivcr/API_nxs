from database_models.brand_model import BrandModel
from database_models.car_model import ModelCarModel
from services.brands import brand_service
from decimal import Decimal
from unittest.mock import patch


class TestBrandServiceConfig:
    obj_brand = BrandModel(id=1, name="Aston Martin")
    obj_model = ModelCarModel(
        id=1, name="Romero", average_price=Decimal(100000), brand_id=1
    )

    @patch("managers.models.ModelsManager.get_models")
    def test_struct_response_brand_service(self, mock_response):
        """Test struct response method."""
        mock_response.return_value = [self.obj_model]
        response = brand_service._struct_response(data=[self.obj_brand])
        assert isinstance(response, list) is True
        assert len(response) == 1
        assert response[0]["nombre"] == "Aston Martin"

    def test_control_response_brand_service(self):
        """Test control response method."""
        response = brand_service._control_data_type(data=[self.obj_brand])
        assert isinstance(response, list) is True
        assert isinstance(response[0], dict) is True
        assert response[0]["name"] == "Aston Martin"
