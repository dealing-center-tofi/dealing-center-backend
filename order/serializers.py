from rest_framework import serializers
from django.db import transaction

from system_auth.serializers import SystemUserSerializer
from currencies.serializers import CurrencyPairSerializer, CurrencyPairValueSerializer
from currencies.models import CurrencyPair, CurrencyPairValue
from .models import Order
from .exceptions import TooMuchCostsValidationError


class OrderSerializer(serializers.ModelSerializer):
    user = SystemUserSerializer(read_only=True)
    currency_pair = CurrencyPairSerializer(read_only=True)
    currency_pair_id = serializers.PrimaryKeyRelatedField(
        queryset=CurrencyPair.objects.all(),
        write_only=True,
        required=True
    )
    start_value = CurrencyPairValueSerializer(read_only=True)
    end_value = CurrencyPairValueSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'currency_pair_id', 'currency_pair', 'status', 'type', 'start_time',
                  'start_value', 'end_time', 'end_value', 'amount')
        extra_kwargs = {'status': {'read_only': True}, 'start_time': {'read_only': True},
                        'end_time': {'read_only': True}}

    def create(self, validated_data):
        currency_pair = validated_data.pop('currency_pair_id')
        validated_data['currency_pair'] = currency_pair
        validated_data['status'] = Order.ORDER_STATUS_OPENED
        start_value = CurrencyPairValue.objects.filter(currency_pair=currency_pair).first()
        validated_data['start_value'] = start_value
        user = validated_data.get('user')
        profit = Order(**validated_data).get_profit(start_value)
        for order in Order.objects.filter(user=user, status=Order.ORDER_STATUS_OPENED):
            currency_pair_value = CurrencyPairValue.objects.filter(currency_pair=order.currency_pair).first()
            profit += order.get_profit(currency_pair_value)
        if user.account.amount * 0.2 > user.account.amount + profit:
            raise TooMuchCostsValidationError()
        instance = super(OrderSerializer, self).create(validated_data)
        return instance
