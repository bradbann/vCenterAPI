#coding:utf-8
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VMware.settings")
django.setup()

# import tables
from vc.models import urun_task_id

def writeData_to_table_urunTaskID(taskid, vmlist):
    #  task ID and the virtual machine list are written to the database
    for vm in vmlist:
        urun_task_id.objects.create(taskid=taskid, vmlist=vm)

def readData_from_table_urunTaskID(taskid=None):
    # Get the list of virtual machines by task ID
    dt_list = []
    taskid_Data = urun_task_id.objects.all().values("taskid", "vmlist")
    if taskid_Data:
        for dt in taskid_Data:
            if taskid == dt["taskid"]:
                dt_list.append(str(dt["vmlist"]))
        return dt_list
    else:
        return False

def readAll_from_table_urunTaskID():
    '''Query all data'''
    taskID_Data = urun_task_id.objects.all()
    for i in taskID_Data:
        print "UUID:%s %s" % (i.taskid, i.vmlist)

#a = readData_from_table_urunTaskID("f0714efe-3810-4c78-bd7f-6fbbf64f885d")
#print type(a)
#readAll_from_table_urunTaskID()



