# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-21 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_auto_20161005_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='menuIndex',
            field=models.IntegerField(default=0),
        ),
    ]