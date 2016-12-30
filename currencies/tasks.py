import json
from datetime import timedelta, datetime

from celery.schedules import crontab
from celery.task import periodic_task, task
from django.db import models

from currencies.models import CurrencyPair, CurrencyPairValue
from dealing_center_settings.models import Setting
from .currency_generator import generator
from .currency_history_generator import generate_history_for_currency_pair


def calculate_task_time():
    return json.loads(Setting.objects.get(name='currency_values_generator_period').value)


@periodic_task(run_every=timedelta(**calculate_task_time()))
def generator_task():
    generator()


@periodic_task(run_every=timedelta(minutes=5))
def generate_history():
    for currency_pair in CurrencyPair.objects.all():
        history_for_currency_pair.delay(currency_pair)


@task
def history_for_currency_pair(pair):
    generate_history_for_currency_pair(pair)


@periodic_task(run_every=crontab(hour='0', minute='5'))
def clean_currency_pair_values():
    for currency_pair in CurrencyPair.objects.all():
        yesterday = datetime.now().date() - timedelta(days=1)
        CurrencyPairValue.objects \
            .filter(currency_pair=currency_pair) \
            .filter(creation_time__date__lt=yesterday) \
            .annotate(start_value_count=models.Count('start_value'),
                      end_value_count=models.Count('end_value')) \
            .filter(start_value_count=0, end_value_count=0) \
            .delete()
