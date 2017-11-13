#coding:utf-8
from vc.src.vm_helper import VMInstance
vminstance = VMInstance()

def aVM_ExistChecked(vmname):
    '''Only check whether a virtual machine exists'''
    vmins= vminstance.get_vm_instance_by_name(vmname)
    if vmins is None:
        return {"vmname":vmname, "desc":"vm error", "success":False}
    else:
        return {"vmname":vmname, "desc":"vm active", "success":True}

def vmListExistChecked(vmlist):
    '''Check the virtual machines in the list of virtual machines that exist and which do not'''
    vm_notExist = []
    vm_Exist = []
    for vmname in vmlist:
        vmins = vminstance.get_vm_instance_by_name(vmname)
        if vmins is None:
            dt = {"vmname":vmname, "existsReult":False}
            vm_notExist.append(dt) #The nonexistent virtual machine is stored in the vm_notExist list
        else:
            vm_Exist.append(vmname) #The existing virtual machine is stored in the vm_Exist list
    res = {"exist":vm_Exist, "notExist":vm_notExist}
    return res
