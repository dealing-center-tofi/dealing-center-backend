# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-20 10:48
from __future__ import unicode_literals

from django.db import migrations, models
import system_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('system_auth', '0002_auto_20161120_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='username',
            field=models.CharField(default=system_auth.models.generate, max_length=50, unique=True),
        ),
    ]
