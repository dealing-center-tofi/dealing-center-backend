import json
from datetime import timedelta

from celery.task import periodic_task

from dealing_center_settings.models import Setting
from .currency_generator import generator


def calculate_task_time():
    return json.loads(Setting.objects.get(name='currency_values_generator_period').value)


@periodic_task(run_every=timedelta(**calculate_task_time()))
def generator_task():
    generator()
