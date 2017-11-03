# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#创建表，表名：task_id
class urun_task_id(models.Model):
    taskid = models.CharField(max_length=500)
    vmlist = models.CharField(max_length=1000)

class ps_netlabel(models.Model):
    netlabel = models.CharField(max_length=500)
