# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-02 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vc', '0011_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskid', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('vmlist', models.CharField(max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='Args',
        ),
        migrations.DeleteModel(
            name='Asset',
        ),
        migrations.DeleteModel(
            name='primary_key_test',
        ),
        migrations.DeleteModel(
            name='Temp',
        ),
        migrations.RemoveField(
            model_name='user',
            name='group_relation',
        ),
        migrations.RemoveField(
            model_name='userinfos',
            name='typeid',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='UserInfos',
        ),
        migrations.DeleteModel(
            name='UserType',
        ),
    ]