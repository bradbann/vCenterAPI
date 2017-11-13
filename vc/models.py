# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class urun_task_id(models.Model):
    taskid = models.CharField(max_length=500)
    vmlist = models.CharField(max_length=1000)

class ps_netlabel(models.Model):
    netlabel = models.CharField(max_length=500)

class ps_datastore_host_relation(models.Model):
    datastore = models.CharField(max_length=500)
    esxi = models.CharField(max_length=500)
