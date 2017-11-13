#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

# 导入表
from vc.models import ps_netlabel

def readData_from_table_ps_netlabel():
    '''Read the ps_netlabel table for all data'''
    dt = []
    data = ps_netlabel.objects.all()
    for i in data:
        dt.append(i.netlabel)
    return dt

def emptData_from_table_ps_netlabel():
    '''Empty table data'''
    print "Database table: ps_netlabel is being reset..."
    ps_netlabel.objects.filter().delete()