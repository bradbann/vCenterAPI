#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

# 导入表
from vc.models import ps_netlabel

def readData_from_table_ps_netlabel():
    dt = []
    data = ps_netlabel.objects.all()
    for i in data:
        dt.append(i.netlabel)
    return dt
