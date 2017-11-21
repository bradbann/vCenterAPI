# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Task ID table creation
class urun_task_id(models.Model):
    taskid = models.CharField(max_length=500)
    vmlist = models.CharField(max_length=1000)
