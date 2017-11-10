#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

# 导入表
from vc.models import ps_datastore_host_relation

def readAllData_from_datastore_host_relation():
    """从数据库中读取所有datastor和esxi数据"""
    return ps_datastore_host_relation.objects.all().values("datastore", "esxi")