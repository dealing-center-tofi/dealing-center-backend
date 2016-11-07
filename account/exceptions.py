from rest_framework.serializers import ValidationError


class NoMoneyValidationError(ValidationError):
    def __init__(self):
        super(NoMoneyValidationError, self).__init__('No money')
