from __future__ import absolute_import

from django.conf.urls import include, url
from rest_framework import routers

from .api import AccountViewSet, TransferViewSet


router = routers.DefaultRouter()
router.register(r'account', AccountViewSet, 'account')
router.register(r'transfers', TransferViewSet, 'transfers')


api_patterns = \
    [
        url(r'', include(router.urls)),
    ]
