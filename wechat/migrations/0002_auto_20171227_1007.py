# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 10:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authwechat',
            options={'ordering': ('-id',)},
        ),
        migrations.AddField(
            model_name='authwechat',
            name='grant_dt',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='授权时间'),
        ),
    ]
