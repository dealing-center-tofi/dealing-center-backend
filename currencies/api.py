from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import filters

from .models import CurrencyPair, CurrencyPairValue
from .serializers import CurrencyPairSerializer, CurrencyPairValueSerializer
from filters import CurrencyPairValueFilter


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
