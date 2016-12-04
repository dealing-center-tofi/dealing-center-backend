from rest_framework import serializers

from .models import Currency, CurrencyPair, CurrencyPairValue, CurrencyPairValueHistory


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name', )


class CurrencyPairSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    base_currency = CurrencySerializer()
    quoted_currency = CurrencySerializer()
    last_value = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyPair
        fields = ('id', 'name', 'base_currency', 'quoted_currency', 'last_value')

    def get_name(self, pair):
        return unicode(pair)

    def get_last_value(self, pair):
        value = pair.pair_values.all().first()
        if value:
            serializer = CurrencyPairValueSerializer(pair.pair_values.all().first())
            return serializer.data


class CurrencyPairValueSerializer(serializers.ModelSerializer):
    spread = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyPairValue
        fields = ('bid', 'ask', 'spread', 'creation_time', 'currency_pair')

    def get_spread(self, pair_value):
        return pair_value.ask - pair_value.bid


class CurrencyPairValueHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyPairValueHistory
        fields = ('open', 'close', 'high', 'low', 'period', 'creation_time', 'currency_pair')
