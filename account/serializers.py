from rest_framework import serializers

from .models import Account, Transfer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('amount', )


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('amount', 'transfer_date', 'transfer_type')
