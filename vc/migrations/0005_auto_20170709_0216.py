# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-09 02:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vc', '0004_auto_20170709_0213'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserInfo',
            new_name='UserInfos',
        ),
    ]
