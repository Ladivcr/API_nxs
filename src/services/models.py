from managers.models import models_manager
from pudb import set_trace
class BranService:
    """Class to struct responses from database."""
    def _struct_response(self, data):
        """Method to struct the data."""
        ...

    def list_models(self):
        """Method to control response from request SELECT in database."""
        response = models_manager.get_models()
        set_trace()
        set_trace()
        return response

brand_service = BranService()