from rest_framework import serializers
from .models import Order
from django.db import transaction
from system_auth.serializers import SystemUserSerializer
from currencies.serializers import CurrencyPairSerializer, CurrencyPairValueSerializer
from currencies.models import CurrencyPair, CurrencyPairValue


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
    initial_amount = serializers.FloatField(write_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'currency_pair_id', 'currency_pair', 'status', 'type', 'start_time',
                  'start_value', 'end_time', 'end_value', 'amount', 'initial_amount')
        extra_kwargs = {'status': {'read_only': True}, 'start_time': {'read_only': True},
                        'end_time': {'read_only': True}, 'amount': {'read_only': True}}

    def create(self, validated_data):
        currency_pair = validated_data.pop('currency_pair_id')
        amount = validated_data.pop('initial_amount')
        validated_data['currency_pair'] = currency_pair
        validated_data['status'] = Order.ORDER_STATUS_OPENED
        start_value = CurrencyPairValue.objects.filter(currency_pair=currency_pair).first()
        validated_data['start_value'] = start_value
        with transaction.atomic():
            if validated_data.get('type') == Order.ORDER_TYPE_LONG:
                validated_data['user'].account.change_amount_after_order(-amount)
                amount /= start_value.ask
            else:
                amount *= start_value.bid
            validated_data['amount'] = amount
            instance = super(OrderSerializer, self).create(validated_data)
        return instance
