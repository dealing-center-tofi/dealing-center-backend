import json
from datetime import timedelta

from celery.task import periodic_task, task

from currencies.models import CurrencyPair
from dealing_center_settings.models import Setting
from .currency_generator import generator
from .currency_history_generator import generate_history_for_currency_pair


def calculate_task_time():
    return json.loads(Setting.objects.get(name='currency_values_generator_period').value)


@periodic_task(run_every=timedelta(**calculate_task_time()))
def generator_task():
    generator()


# @periodic_task(run_every=timedelta(minutes=5))
def generate_history():
    for currency_pair in CurrencyPair.objects.all():
        # history_for_currency_pair.delay(currency_pair)
        history_for_currency_pair(currency_pair)


# @task
def history_for_currency_pair(pair):
    generate_history_for_currency_pair(pair)
