# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-13 18:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_currency_pricetousd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='priceToUSD',
            new_name='price_to_usd',
        ),
    ]
