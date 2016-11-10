from rest_framework import serializers

from .models import Currency, CurrencyPair, CurrencyPairValue


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('name', )


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
        fields = ('bid', 'ask', 'spread', 'creation_time')

    def get_spread(self, pair_value):
        return pair_value.bid - pair_value.ask