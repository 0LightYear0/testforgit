# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-22 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0004_activity_menuindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='invalid_tickets',
            field=models.CharField(default='[]', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='used_tickets',
            field=models.CharField(default='[]', max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='valid_tickets',
            field=models.CharField(default='[]', max_length=200),
        ),
    ]
