from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import filters

from dealing_center.utils.pagination import PageSizePagination
from .models import CurrencyPair, CurrencyPairValue, Currency
from .serializers import CurrencyPairSerializer, CurrencyPairValueSerializer, CurrencySerializer
from filters import CurrencyPairValueFilter


class CurrencyViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class CurrencyPairViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencyPairSerializer
    queryset = CurrencyPair.objects.all()


class CurrencyPairValueViewSet(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencyPairValueSerializer
    queryset = CurrencyPairValue.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CurrencyPairValueFilter
    pagination_class = PageSizePagination
