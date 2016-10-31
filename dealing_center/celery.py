from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings


os.environ['DJANGO_SETTINGS_MODULE'] = 'dealing_center.settings'

app = Celery('dealing_center')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
