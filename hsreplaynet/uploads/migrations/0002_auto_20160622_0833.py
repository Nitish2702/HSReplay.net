# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-06-22 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadevent',
            name='error',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='uploadevent',
            name='traceback',
            field=models.TextField(blank=True),
        ),
    ]
