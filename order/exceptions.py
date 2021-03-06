from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings

class TooMuchCostsValidationError(ValidationError):
    def __init__(self):
        super(TooMuchCostsValidationError, self).__init__({
                api_settings.NON_FIELD_ERRORS_KEY: ['Too much costs in orders.'],
            })
