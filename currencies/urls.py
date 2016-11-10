from __future__ import absolute_import

from django.conf.urls import include, url
from rest_framework import routers

from .api import CurrencyPairViewSet, CurrencyPairValueViewSet


router = routers.DefaultRouter()
router.register(r'currency_pairs', CurrencyPairViewSet, 'currency_pairs')
router.register(r'currency_pair_values', CurrencyPairValueViewSet, 'currency_pair_values')


api_patterns = \
    [
        url(r'', include(router.urls)),
    ]
