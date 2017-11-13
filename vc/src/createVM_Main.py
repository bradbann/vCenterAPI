#coding:utf-8
import pickle
import time
from vc.src.vm_helper import VMAction
from vc.src.vmExistChecked import aVM_ExistChecked
from db import table_urun_task_id

vmaction = VMAction()

def checkRepeat_VM_Name(vmlist):
    '''Check the VM that the virtual machine name repeats, the duplicate VM name is
    returned to the caller, and the virtual machine name that is available is passed
    in to create the virtual machine function
    '''
    repeat_vm_list = []
    able_vm_list = []
    for vm in vmlist:
        r = aVM_ExistChecked(vm)
        if r['success'] == False:
            able_vm_list.append(r["vmname"])
        else:
            repeat_vm_list.append(r["vmname"])
    dt = {"availableVMName":able_vm_list, "repeatVMName":repeat_vm_list}
    return dt

def taskBinding(taskID, vmlist):
    '''The task ID is bound to the virtual machine list, and queries are made by the
    task ID when the query iscreated successfully
    '''
    table_urun_task_id.writeData_to_table_urunTaskID(taskid=taskID, vmlist=vmlist) #  task ID and the virtual list are written to the database

def create_vm_main(vmlist=None, template_name=None, resourceid=None, hostid=None, datastoreid=None, number=None, nameprefix=None, taskID=None):

    taskBinding(taskID, vmlist) #Task ID and virtual machine list binding

    # Create a virtual machine specifying a name, such as create a vmlist=["vm1"], or multiple vmlist=["vm2", "vm3"]
    if vmlist != None:
        for vm in vmlist:
            vmaction.vm_from_template_create(name=vm, template_name=template_name, pool=resourceid, esx=hostid, lun=datastoreid)

    # Creates a specified number of virtual machines and passes the name suffix to create
    if number != None or nameprefix != None:
        for vm in vmlist:
            vmaction.vm_from_template_create(name=vm, template_name=template_name, pool=resourceid, esx=hostid, lun=datastoreid)
