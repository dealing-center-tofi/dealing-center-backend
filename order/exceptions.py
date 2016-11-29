from rest_framework.serializers import ValidationError


class TooMuchCostsValidationError(ValidationError):
    def __init__(self):
        super(TooMuchCostsValidationError, self).__init__('Too much costs in orders.')
