from django_filters import rest_framework as filters

from .models import CurrencyPairValue, CurrencyPair


class CurrencyPairValueFilter(filters.FilterSet):
    currency_pair = filters.ModelChoiceFilter(queryset=CurrencyPair.objects.all())

    class Meta:
        model = CurrencyPairValue
        fields = ('currency_pair', )
