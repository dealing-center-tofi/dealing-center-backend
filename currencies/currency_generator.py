from .models import Currency, CurrencyPair, CurrencyPairValue
from random import random


def get_random(m=1, d=0.02, n=12):
    sum_r = sum([random() for _ in xrange(n)])
    return m + (d * (12 / n)**0.5 * (sum_r - n/2))


def generator():
    currencies = Currency.objects.all()
    for currency in currencies:
        currency.price_to_usd *= get_random()
        if currency.name == 'USD':
            usd_price = currency.price_to_usd

    for currency in currencies:
        currency.price_to_usd /= usd_price
        currency.save()

    currencies_for_create = []
    for pair in CurrencyPair.objects.all():
        price = pair.quoted_currency.price_to_usd / pair.base_currency.price_to_usd
        currencies_for_create.append(
            CurrencyPairValue(currency_pair=pair, ask=price * 1.005, bid=price * 0.995)
        )
    CurrencyPairValue.objects.bulk_create(currencies_for_create)
