# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vc', '0008_asset'),
    ]

    operations = [
        migrations.CreateModel(
            name='primary_key_test',
            fields=[
                ('ID', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Asset',
        ),
    ]
