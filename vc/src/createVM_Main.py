#coding:utf-8
import pickle
import time
from vc.src.vm_helper import VMAction
from vc.src.vmExistChecked import aVM_ExistChecked
from db import table_urun_task_id

vmaction = VMAction()

def checkRepeat_VM_Name(vmlist):
    # 检查虚拟机名称重复的VM，重复的VM名称返回给调用方，可用的虚拟机名称传入创建虚拟机函数
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
    #任务ID和虚拟机列表绑定，查询是否创建成功时，通过任务ID进行查询
    # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # dt = {taskID: {"vmlist": vmlist, "date":date}}  # 用UUID作为key
    # try:
    #     taskID_vmlist = open("taskID_vmlist.pk1", 'ab')
    # except Exception:
    #     print "Task ID, write database error"
    # else:
    #     pickle.dump(dt, taskID_vmlist) #将数据用pickle模块进行序列化存储
    #     taskID_vmlist.close()
    table_urun_task_id.writeData_to_table_urunTaskID(taskid=taskID, vmlist=vmlist) # 任务ID和虚拟列表写入数据库

def create_vm_main(vmlist=None, template_name=None, resourceid=None, hostid=None, datastoreid=None, number=None, nameprefix=None, taskID=None):

    taskBinding(taskID, vmlist) #任务ID和虚拟机列表绑定

    # 创建指定名称的虚拟机，如创建一台vmlist=["vm1"],或 多台vmlist=["vm2", "vm3"]
    if vmlist != None:
        for vm in vmlist:
            vmaction.vm_from_template_create(name=vm, template_name=template_name, pool=resourceid, esx=hostid, lun=datastoreid)
    # 创建指定数量的虚拟机，并传入名称后缀进行创建
    if number != None or nameprefix != None:
        for vm in vmlist:
            vmaction.vm_from_template_create(name=vm, template_name=template_name, pool=resourceid, esx=hostid, lun=datastoreid)
