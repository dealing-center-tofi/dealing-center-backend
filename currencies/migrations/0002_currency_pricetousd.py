# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-13 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='priceToUSD',
            field=models.FloatField(default=0),
        ),
    ]
