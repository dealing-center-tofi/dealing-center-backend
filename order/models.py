from __future__ import unicode_literals

from django.db import models
from django.db import transaction
from django.core import validators
from django.db.models import Q
from django.utils import timezone

from system_auth.models import SystemUser
from currencies.models import CurrencyPair, CurrencyPairValue


class Order(models.Model):
    ORDER_STATUS_OPENED = 1
    ORDER_STATUS_CLOSED = 2
    ORDER_STATUS_CHOICES = (
        (ORDER_STATUS_OPENED, 'Opened'),
        (ORDER_STATUS_CLOSED, 'Closed'),
    )

    ORDER_TYPE_BUY = 1
    ORDER_TYPE_SELL = 2
    ORDER_TYPE_CHOICES = (
        (ORDER_TYPE_BUY, 'buy'),
        (ORDER_TYPE_SELL, 'sell'),
    )

    user = models.ForeignKey(SystemUser)
    currency_pair = models.ForeignKey(CurrencyPair)
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES)
    type = models.SmallIntegerField(choices=ORDER_TYPE_CHOICES)
    start_time = models.DateTimeField(auto_now_add=True)
    start_value = models.ForeignKey(CurrencyPairValue, related_name='start_value')
    end_time = models.DateTimeField(null=True)
    end_value = models.ForeignKey(CurrencyPairValue, related_name='end_value', null=True)
    amount = models.FloatField(validators=[validators.MinValueValidator(0.01)])
    end_profit = models.FloatField(null=True, blank=True)

    def close(self):
        self.end_time = timezone.now()
        end_value = CurrencyPairValue.objects.filter(currency_pair=self.currency_pair).first()
        self.end_value = end_value
        self.status = Order.ORDER_STATUS_CLOSED
        with transaction.atomic():
            amount = self.get_profit(end_value)
            self.user.account.change_amount_after_order(amount, raise_exception=False)
            self.end_profit = amount
            self.save()

    def get_profit(self, currency_pair_value):
        amount = self.amount
        if self.type == self.ORDER_TYPE_BUY:
            debt_amount = amount * self.start_value.ask
            amount -= debt_amount / currency_pair_value.bid
            rest_currency = self.currency_pair.base_currency
        else:
            amount *= (self.start_value.bid - currency_pair_value.ask)
            rest_currency = self.currency_pair.quoted_currency
        user_currency = self.user.account.currency
        if rest_currency != user_currency:
            sub_pair = CurrencyPair.objects.get(
                Q(base_currency=rest_currency,
                  quoted_currency=user_currency) |
                Q(base_currency=user_currency,
                  quoted_currency=rest_currency)
            )
            sub_pair = CurrencyPairValue.objects.filter(currency_pair=sub_pair).first()
            if sub_pair.currency_pair.base_currency == rest_currency:
                amount *= sub_pair.bid
            else:
                amount /= sub_pair.ask
        return amount

    def __unicode__(self):
        return '%s [%s]: %s' % (self.get_type_display(), self.get_status_display(), self.start_time)
