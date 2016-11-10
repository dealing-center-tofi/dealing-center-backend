from __future__ import unicode_literals

from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=128)

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
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-creation_time', )

    def __unicode__(self):
        return '%s - %s' % (self.bid, self.ask)
