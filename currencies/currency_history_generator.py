from datetime import timedelta

from django.utils import timezone

from .models import CurrencyPair, CurrencyPairValue, CurrencyPairValueHistory


PERIOD_RANGES = {
    CurrencyPairValueHistory.PERIOD_5_MINUTES: timedelta(minutes=5),
    CurrencyPairValueHistory.PERIOD_15_MINUTES: timedelta(minutes=15),
    CurrencyPairValueHistory.PERIOD_30_MINUTES: timedelta(minutes=30),
    CurrencyPairValueHistory.PERIOD_HOUR: timedelta(hours=1),
    CurrencyPairValueHistory.PERIOD_4_HOURS: timedelta(hours=4),
    CurrencyPairValueHistory.PERIOD_1_DAY: timedelta(days=1),
    CurrencyPairValueHistory.PERIOD_1_WEEK: timedelta(weeks=1)
}


def currency_history_generator(pair, period, last_creation_time):
    if last_creation_time is None:
        first_value_ever = CurrencyPairValue.objects.last()
        if first_value_ever is None:
            return []
        start_creation_time = first_value_ever.creation_time.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start_creation_time = last_creation_time + PERIOD_RANGES[period]

    if period == CurrencyPairValueHistory.PERIOD_5_MINUTES:
        return generate_for_5_minutes_period(pair, start_creation_time)
    else:
        return generate_for_other_periods(pair, period, start_creation_time)


def generate_for_other_periods(pair, period, start_creation_time):
    period_range = PERIOD_RANGES[period]

    generated_array = []
    while start_creation_time <= timezone.now() - period_range:
        data_range = [start_creation_time,
                      start_creation_time + period_range - PERIOD_RANGES[CurrencyPairValueHistory.PERIOD_5_MINUTES]]

        pair_values_qs = CurrencyPairValueHistory.objects.filter(currency_pair=pair, creation_time__range=data_range,
                                                                 period=CurrencyPairValueHistory.PERIOD_5_MINUTES)
        high_bound_qs = pair_values_qs.order_by('-high').values_list('high', flat=True)
        low_bound_qs = pair_values_qs.order_by('low').values_list('low', flat=True)

        if pair_values_qs.exists():
            first, last = pair_values_qs.last().open, pair_values_qs.first().close
            high, low = high_bound_qs.first(), low_bound_qs.first()

            generated_array.append(CurrencyPairValueHistory(open=first, high=high, low=low, close=last,
                                                            creation_time=start_creation_time, period=period,
                                                            currency_pair=pair))
        start_creation_time += period_range
    return generated_array


def generate_for_5_minutes_period(pair, start_creation_time):
    period = CurrencyPairValueHistory.PERIOD_5_MINUTES
    period_range = PERIOD_RANGES[period]

    generated_array = []
    while start_creation_time <= timezone.now() - period_range:
        data_range = [start_creation_time, start_creation_time + period_range]

        pair_values_qs = CurrencyPairValue.objects.filter(currency_pair=pair, creation_time__range=data_range) \
            .values_list('ask', flat=True)
        ordered_by_ask = pair_values_qs.order_by('-ask')

        if pair_values_qs.exists():
            first, last = pair_values_qs.last(), pair_values_qs.first()
            high, low = ordered_by_ask.first(), ordered_by_ask.last()

            generated_array.append(CurrencyPairValueHistory(open=first, high=high, low=low, close=last,
                                                            creation_time=start_creation_time, period=period,
                                                            currency_pair=pair))
        start_creation_time += period_range
    return generated_array


def generate_for_currency_pair(pair):
    for period in map(lambda x: x[0], CurrencyPairValueHistory.period_choices):
        last_history_value = CurrencyPairValueHistory.objects.filter(currency_pair=pair, period=period).first()
        if last_history_value is None \
                or last_history_value.creation_time <= timezone.now() - PERIOD_RANGES[period]:

            last_value_creation_time = last_history_value.creation_time if last_history_value else None
            values_for_create = currency_history_generator(pair, period, last_value_creation_time)
            if values_for_create:
                count = len(CurrencyPairValueHistory.objects.bulk_create(values_for_create))
                print count
            print 'created for %s and period %s' % (pair.id, period)
            print '------------------'


# task every 5 minutes (1 minute)
def generate_1():
    for currency_pair in CurrencyPair.objects.all():
        generate_for_currency_pair(currency_pair)
