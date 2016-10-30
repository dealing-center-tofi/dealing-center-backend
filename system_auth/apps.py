from __future__ import unicode_literals

from django.apps import AppConfig


class SystemAuthConfig(AppConfig):
    name = 'system_auth'

    def ready(self):
        from system_auth import signals
