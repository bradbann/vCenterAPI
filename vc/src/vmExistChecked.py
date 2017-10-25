#coding:utf-8
from vc.src.vm_helper import VMInstance
vminstance = VMInstance()

def aVM_ExistChecked(vmname):
    #只检查一台虚拟机是否存在
    vmins= vminstance.get_vm_instance_by_name(vmname)
    if vmins is None:
        return {"vmname":vmname, "desc":"vm error", "success":False}
    else:
        return {"vmname":vmname, "desc":"vm active", "success":True}

def vmListExistChecked(vmlist):
    #检查一组虚拟机列表中的虚拟机哪些是存在，哪些不存在
    vm_notExist = []
    vm_Exist = []
    for vmname in vmlist:
        vmins = vminstance.get_vm_instance_by_name(vmname)
        if vmins is None:
            dt = {"vmname":vmname, "existsReult":False}
            vm_notExist.append(dt) #不存在的虚拟机存入vm_notExist列表
        else:
            vm_Exist.append(vmname) #存在的虚拟机存入vm_Exist列表
    res = {"exist":vm_Exist, "notExist":vm_notExist}
    return res
