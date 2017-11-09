#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

# 导入表
from vc.models import ps_netlabel

def readData_from_table_ps_netlabel():
    '''读取ps_netlabel表所有数据'''
    dt = []
    data = ps_netlabel.objects.all()
    for i in data:
        dt.append(i.netlabel)
    return dt

def emptData_from_table_ps_netlabel():
    '''清空表中的数据'''
    print "数据库表：ps_netlabel 正在重置..."
    ps_netlabel.objects.filter().delete()