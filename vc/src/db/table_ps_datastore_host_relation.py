#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

#  import table
from vc.models import ps_datastore_host_relation

def readAllData_from_datastore_host_relation():
    """Read all datastor and esxi data from the database"""
    return ps_datastore_host_relation.objects.all().values("datastore", "esxi")