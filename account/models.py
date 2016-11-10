from __future__ import unicode_literals

from django.core import validators
from django.db import models

from currencies.models import Currency
from system_auth.models import SystemUser

from .exceptions import NoMoneyValidationError


class Account(models.Model):
    user = models.OneToOneField(SystemUser)
    currency = models.ForeignKey(Currency)
    amount = models.FloatField(default=0)

    def __unicode__(self):
        return 'Account for %s' % self.user.get_full_name()

    def change_amount_after_transfer(self, transfer):
        if transfer.transfer_type == Transfer.TRANSFER_TYPE_PUT:
            self.amount += transfer.amount
        elif transfer.transfer_type == Transfer.TRANSFER_TYPE_WITHDRAW:
            if self.amount < transfer.amount:
                raise NoMoneyValidationError()
            self.amount -= transfer.amount
        self.save()


class Transfer(models.Model):
    TRANSFER_TYPE_PUT = 1
    TRANSFER_TYPE_WITHDRAW = 2
    TRANSFER_TYPE_CHOICES = (
        (TRANSFER_TYPE_PUT, 'Put'),
        (TRANSFER_TYPE_WITHDRAW, 'Withdraw'),
    )

    account = models.ForeignKey(Account, related_name='transfers')
    amount = models.FloatField(default=0, validators=[validators.MinValueValidator(0)])
    transfer_date = models.DateTimeField(auto_now_add=True)
    transfer_type = models.SmallIntegerField(choices=TRANSFER_TYPE_CHOICES)

    def __unicode__(self):
        return "%s - %s - %s" % (self.account, self.get_transfer_type_display(), self.transfer_date)
