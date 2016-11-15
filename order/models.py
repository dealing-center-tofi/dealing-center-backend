from __future__ import unicode_literals

from django.db import models
from system_auth.models import SystemUser
from currencies.models import CurrencyPair, CurrencyPairValue


class Order(models.Model):
    ORDER_STATUS_OPENED = 1
    ORDER_STATUS_CLOSED = 2
    ORDER_STATUS_CHOICES = (
        (ORDER_STATUS_OPENED, 'Opened'),
        (ORDER_STATUS_CLOSED, 'Closed'),
    )

    ORDER_TYPE_LONG = 1
    ORDER_TYPE_SHORT = 2
    ORDER_TYPE_CHOICES = (
        (ORDER_TYPE_LONG, 'Long'),
        (ORDER_TYPE_SHORT, 'Short'),
    )

    user = models.ForeignKey(SystemUser)
    currency_pair = models.ForeignKey(CurrencyPair)
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES)
    type = models.SmallIntegerField(choices=ORDER_TYPE_CHOICES)
    start_time = models.DateTimeField(auto_now_add=True)
    start_value = models.ForeignKey(CurrencyPairValue, related_name='start_value')
    end_time = models.DateTimeField(null=True)
    end_value = models.ForeignKey(CurrencyPairValue, related_name='end_value', null=True)
    amount = models.FloatField()

    def __unicode__(self):
        return '%s [%s]: %s' % (self.get_type_display(), self.get_status_display(), self.start_time)
