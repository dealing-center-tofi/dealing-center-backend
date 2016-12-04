from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Currency(models.Model):
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=128)
    price_to_usd = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __unicode__(self):
        return self.name


class CurrencyPair(models.Model):
    base_currency = models.ForeignKey(Currency, related_name='pairs_where_base')
    quoted_currency = models.ForeignKey(Currency, related_name='pairs_where_quoted')

    def __unicode__(self):
        return '%s/%s' % (self.base_currency, self.quoted_currency)


class CurrencyPairValue(models.Model):
    currency_pair = models.ForeignKey(CurrencyPair, related_name='pair_values')
    bid = models.FloatField()
    ask = models.FloatField()
    creation_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        is_new = not bool(self.id)
        if is_new and not self.creation_time:
            self.creation_time = timezone.now()
        return super(CurrencyPairValue, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-creation_time', )

    def __unicode__(self):
        return '%s - %s' % (self.bid, self.ask)


class CurrencyPairValueHistory(models.Model):
    PERIOD_5_MINUTES = 1
    PERIOD_15_MINUTES = 2
    PERIOD_30_MINUTES = 3
    PERIOD_HOUR = 4
    PERIOD_4_HOURS = 5
    PERIOD_1_DAY = 6
    PERIOD_1_WEEK = 7

    period_choices = (
        (PERIOD_5_MINUTES, '5 minutes'),
        (PERIOD_15_MINUTES, '15 minutes'),
        (PERIOD_30_MINUTES, '30 minutes'),
        (PERIOD_HOUR, '1 hour'),
        (PERIOD_4_HOURS, '4 hours'),
        (PERIOD_1_DAY, '1 day'),
        (PERIOD_1_WEEK, '1 week'),
    )

    currency_pair = models.ForeignKey(CurrencyPair, related_name='pair_values_history')
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    creation_time = models.DateTimeField()
    period = models.SmallIntegerField(choices=period_choices)

    def save(self, *args, **kwargs):
        is_new = not bool(self.id)
        if is_new and not self.creation_time:
            self.creation_time = timezone.now()
        return super(CurrencyPairValueHistory, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-creation_time',)

    def __unicode__(self):
        return '%s - %s' % (self.currency_pair, self.creation_time)
