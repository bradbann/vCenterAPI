#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

# 导入表
from vc.models import urun_task_id

def writeData_to_table_urunTaskID(taskid, vmlist):
    urun_task_id.objects.create(taskid=taskid, vmlist=vmlist)

def readData_from_table_urunTaskID(taskid):
    dt = None
    taskid_Data = urun_task_id.objects.filter(taskid__contains=taskid)
    if taskid_Data:
        for i in taskid_Data:
            temp_data = i.vmlist
            t = temp_data.replace('u\'','\'').replace("['", "").replace("'", "").replace("]","").replace(",", "")
            dt = list(str(t).split(" "))
        return dt
    else:
        return False

def readAll_from_table_urunTaskID():
    taskID_Data = urun_task_id.objects.all()
    for i in taskID_Data:
        print "UUID:%s %s" % (i.taskid, i.vmlist)

# a = readData_from_table_urunTaskID("f0714efe-3810-4c78-bd7f-6fbbf64f885d")
# print a
#readAll_from_table_urunTaskID()

