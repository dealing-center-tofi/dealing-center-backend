from __future__ import absolute_import

from django.conf.urls import include, url
from rest_framework import routers

from .api import OrderViewSet


router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, 'orders')


api_patterns = \
    [
        url(r'', include(router.urls)),
    ]
