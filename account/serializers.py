from rest_framework import serializers

from currencies.serializers import CurrencySerializer
from .models import Account, Transfer


class AccountSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('amount', 'currency')


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('amount', 'transfer_date', 'transfer_type')
