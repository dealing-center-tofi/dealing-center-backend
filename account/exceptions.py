from rest_framework.serializers import ValidationError


class NoMoneyValidationError(ValidationError):
    def __init__(self):
        super(NoMoneyValidationError, self).__init__('No money')


class TooMuchCostsValidationError(ValidationError):
    def __init__(self):
        super(TooMuchCostsValidationError, self).__init__('Too much costs in orders.')