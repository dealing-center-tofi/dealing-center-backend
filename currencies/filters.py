from django_filters import rest_framework as filters

from .models import CurrencyPairValue, CurrencyPair, CurrencyPairValueHistory


class CurrencyPairValueFilter(filters.FilterSet):
    currency_pair = filters.ModelChoiceFilter(queryset=CurrencyPair.objects.all())

    class Meta:
        model = CurrencyPairValue
        fields = ('currency_pair', )


class CurrencyPairValueHistoryFilter(filters.FilterSet):
    currency_pair = filters.ModelChoiceFilter(queryset=CurrencyPair.objects.all())
    creation_time_min = filters.DateTimeFilter(name='creation_time', lookup_expr='gte')
    creation_time_max = filters.DateTimeFilter(name='creation_time', lookup_expr='lte')

    class Meta:
        model = CurrencyPairValueHistory
        fields = ('currency_pair', 'period', 'creation_time_min', 'creation_time_max')
