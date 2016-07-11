# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-07-10 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20160708_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='globalgameplayer',
            name='duplicated',
        ),
        migrations.AddField(
            model_name='globalgameplayer',
            name='real_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='Real name'),
        ),
    ]