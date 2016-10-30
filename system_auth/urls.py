from __future__ import absolute_import

from django.conf.urls import include, url
from rest_framework import routers

from .api import SystemUserViewSet, AuthViewSet


router = routers.DefaultRouter()
router.register(r'users', SystemUserViewSet, 'users')
router.register(r'auth', AuthViewSet, 'auth')


api_patterns = \
    [
        url(r'', include(router.urls)),
    ]
