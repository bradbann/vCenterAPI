# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import uuid
import json
from threading import Thread
from src.vm_helper import VMInstance, VMAction
from src.device_info.vm_info import VM_Info
from src.device_info.public_base_info import BaseInfo
from src.vmExistChecked import aVM_ExistChecked, vmListExistChecked
from src.createVM_Main import create_vm_main, checkRepeat_VM_Name
from src.get_vm_create_status import get_vmCreate_status
from src.powercli.update_data_handler import update_netlabel, update_datastore_And_esxi_relation

vminstance = VMInstance()
vmaction = VMAction()
vminfo = VM_Info()
baseinfo = BaseInfo()

def get_vmName(request):
    '''Query only the name of the virtual machine for administrator use'''
    if request.method == "POST":
        data = json.loads(request.body)
        getmode = data.get("getmode", None)
        dt = vminstance.get_filter_vm(getmode)
        dd = []
        for i in dt:
            dd.append(i["name"])
        return HttpResponse(json.dumps(dd))
    else:
        return HttpResponse("Not allowed to get model")

def get_VM_CreateStatus(request):
    '''Query the virtual machine creation status'''
    if request.method == "POST":
        data = json.loads(request.body)
        taskID = data.get("taskID", None)
        result = get_vmCreate_status(taskID=taskID)
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse("Not allowed to get model")

def info_vm_basic(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            getmode = data.get("getmode")
            datacenter = data.get("datacenter", None)
            cluster = data.get("cluster",None)
            resource_pool = data.get("resource_pool", None)
            vmname = data.get("vmname", None)
            vmlist = data.get("vmlist", None)
            if getmode == "NAMEMODE":
                if vmname:
                    checkRes = aVM_ExistChecked(vmname)
                    if checkRes['success'] != True:
                        error_info = {"success": False, "data": "null", "errorCode": 5561, "errorDesc": " no virtual machine"}
                        return HttpResponse(json.dumps(error_info))
                    vm_instance = vminstance.get_vm_instance_by_name(vmname)
                    dt = vminfo.get_vm_basic_info(vm_instance)
                    res = {"success": True, "data":dt, "errorCode":"null", "errorDesc":"null"}
                    return HttpResponse(json.dumps(res))
                else:
                    error_info = {"success": False, "data": "null", "errorCode":467731, "errorDesc": "Must provide parameters: vmname=VM name"}
                    return HttpResponse(json.dumps(error_info))

            if getmode in ['ALL', 'POWER_ON', 'POWER_OFF', 'SUSPENDED']:
                vm_instance = vminstance.get_filter_vm(getmode, datacenter=datacenter, cluster=cluster, resource_pool=resource_pool)
                dt = vminfo.get_vm_basic_info(vm_instance)
                if len(dt) == 0:
                    error_info = {"success": False, "data": "null", "errorCode":221076, "errorDesc": "not data"}
                    return HttpResponse(json.dumps(error_info))
                else:
                    res = {"success": True, "data": dt, "errorCode": "null", "errorDesc": "null"}
                    return HttpResponse(json.dumps(res))

            if getmode == "aGroupVM":
                if vmlist == None:
                    error_info = {"success": False, "data":"null", "errorCode":3409, "errorDesc": "A list of virtual machines must be provided"}
                    return HttpResponse(json.dumps(error_info))
                vm_notExist_list = None
                vmCheckedResult = vmListExistChecked(vmlist)
                if vmCheckedResult.get("notExist", None):
                    vm_notExist_list = vmCheckedResult.get("notExist", None)
                else: vm_notExist_list = []

                new_vmlist = None
                if vmCheckedResult.get("exist", None):
                    new_vmlist = vmCheckedResult.get("exist", None)
                else: new_vmlist = []

                vm_info = None
                if new_vmlist:
                    if isinstance(new_vmlist, list):
                        if new_vmlist:
                            vm_instance = vminstance.get_aGroupVMInstance(new_vmlist)
                            vm_info = vminfo.get_vm_basic_info(vm_instance)
                        else:
                            error = {"success": False, "data": "null", "errorCode": 77890,"errorDesc": " virtual machine list cannot be empty"}
                            return HttpResponse(json.dumps(error))
                    else:
                        error = {"success": False, "data": "null", "errorCode": 982301, "errorDesc": "For a specified number of virtual machine operations, a list type must be passed in"}
                        return HttpResponse(json.dumps(error))
                else:
                    error = {"success": False, "data": "null", "errorCode": 37642, "errorDesc":"There is no virtual machine available"}
                    return HttpResponse(json.dumps(error))
                if vm_info == False:
                    error_info = {"success": False, "data": "null", "errorCode": 109234,"errorDesc": "No virtual machine information"}
                    return HttpResponse(json.dumps(error_info))
                else:
                    dt = {"availableVM":new_vmlist, "errorVM":vm_notExist_list, "vmData":vm_info}
                    result = {"success": True, "data": dt, "errorCode":"null", "errorDesc":"null"}
                    return HttpResponse(json.dumps(result))
        else:
            return HttpResponse("Not allowed to get model")
    except Exception,e:
        return e

def info_public_data(request):
    dt = baseinfo.main_base_data()
    result = {"success": True, "data": dt, "errorCode": "null", "errorDesc": "null"}
    baseinfo.del_baseData_List()
    return HttpResponse(json.dumps(result))

def update_netlabels(request):
    result = update_netlabel()
    if result:
        result = {"success": True, "data":"", "errorCode": "null", "errorDesc": "null"}
        return HttpResponse(json.dumps(result))
    else:
        error_info = {"success": False, "data":"", "errorCode":901020678, "errorDesc": "Network tag gets update failed"}
        return HttpResponse(json.dumps(error_info))

def update_datastoreAndEsxi_relation(request):
    result = update_datastore_And_esxi_relation()
    if result:
        result = {"success": True, "data": "", "errorCode": "null", "errorDesc": "null"}
        return HttpResponse(json.dumps(result))
    else:
        error_info = {"success": False, "data": "", "errorCode": 11223309,"errorDesc": "update failed"}
        return HttpResponse(json.dumps(error_info))

def vm_public_action(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            mode = data.get("mode", None)
            vmname = data.get("vmname", None)
            vmpath = data.get("vmpath", None)
            action_type = data.get("action_type", None)
            filters = data.get("filters", None)
            datacenter = data.get("datacenter", None)
            cluster = data.get("cluster", None)
            resource_pool = data.get("resource_pool",None)
            snapshot_name = data.get("snapshot_name", None)
            snapshot_describe = data.get("snapshot_describe", None)
            clone_vmname = data.get("clone_vmname",None)
            vdisk_name = data.get("vdisk_name", None)
            vdisk_size = data.get("vdisk_size", None)
            datastore_name = data.get("datastore_name", None)
            unit_number = data.get("unit_number", None)
            memory_gb = data.get("memory_gb", None)
            cpu_number = data.get("cpu_number", None)
            cpu_core = data.get("cpu_core", None)
            nic_name = data.get("nic_name", None)
            network_label = data.get("network_label", None)
            to_host = data.get('to_host', None)
            vmlist = data.get("vmlist", None)

            if vmname:
                result = aVM_ExistChecked(vmname)
                if result["success"] == False:
                    errorDesc = "Virtual machine: %s does not exist" % vmname
                    res = {"success": False, "data": "null", "errorCode": 45098, "errorDesc": errorDesc}
                    return HttpResponse(json.dumps(res))

            vm_instance = ""

            if mode == None:
                if vmname != None:
                    vm_instance = vminstance.get_vm_instance_by_name(vmname)
                if vmpath != None:
                    vm_instance = vminstance.get_vm_instance_by_path(vmpath)

            if mode == "batch":
                if filters == None:
                    msg = "'filters=' parameters must be, because you select the 'batch'," \
                          "Filters = value: 'ALL', 'POWER_ON', 'POWER_OFF', 'SUSPENDED'"
                    return HttpResponse(msg)
                else:
                    vm_instance = vminstance.get_filter_vm(filters, datacenter=None, cluster=None, resource_pool=None)

            if mode == "aGroupVM":
                if vmlist == None:
                    error = {"success": False, "data": "null", "errorCode": 9010020907,"errorDesc": "vmlist parameter is a must"}
                    return HttpResponse(json.dumps(error))

                if not isinstance(vmlist, list):
                    error = {"success": False, "data": "null", "errorCode": 5010201,"errorDesc": "vmlist should be an array type"}
                    return HttpResponse(json.dumps(error))

                vm_notExist_list = None
                vmCheckedResult = vmListExistChecked(vmlist)
                if vmCheckedResult.get("notExist", None):
                    vm_notExist_list = vmCheckedResult.get("notExist", None)
                else: vm_notExist_list = []

                new_vmlist = None
                if vmCheckedResult.get("exist", None):
                    new_vmlist = vmCheckedResult.get("exist", None)
                else: new_vmlist = []

                if vm_notExist_list:
                    res = {"success": False, "data":vm_notExist_list, "errorCode":2315, "errorDesc": "Discover that there is a virtual machine that does not exist and cannot continue"}
                    return HttpResponse(json.dumps(res))
                if new_vmlist:
                    if isinstance(new_vmlist, list):
                        if new_vmlist:
                            vm_instance = vminstance.get_aGroupVMInstance(new_vmlist)
                        else:
                            error = {"success": False, "data": "null", "errorCode": 77890,"errorDesc": " virtual machine list cannot be empty"}
                            return HttpResponse(json.dumps(error))
                    else:
                        error = {"success": False, "data": "null", "errorCode": 982301, "errorDesc": "For a specified number of virtual machine operations, a list type must be passed in"}
                        return HttpResponse(json.dumps(error))
                else:
                    error = {"success": False, "data": "null", "errorCode": 9009, "errorDesc":"There is no virtual machine available"}
                    return HttpResponse(json.dumps(error))

            if action_type == "power_on":
                result = vmaction.vm_power_on(vm_instance)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 72509, "errorDesc": "power on failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "power_off":
                result = vmaction.vm_power_off(vm_instance)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 62519, "errorDesc": "power off failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "reset":
                result = vmaction.vm_reset(vm_instance)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 52529, "errorDesc": "vm reset failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "suspend":
                result = vmaction.vm_power_suspend(vm_instance)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 22599, "errorDesc": "suspend failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "restore_current":
                result = vmaction.revert_vm_current_snapshot(vm_instance)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 86509, "errorDesc": "Restore snapshot failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "revert_specified":
                if snapshot_name == None:
                    return HttpResponse("Must specify the snapshot name (snapshot_name='snapshot name')")
                result = vmaction.revert_vm_specified_snapshot(vm_instance, snapshot_name)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 86509,"errorDesc": "Restore snapshot failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode":"null","errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "create_snapshot":
                if snapshot_name == None:
                    return HttpResponse("Must specify the snapshot name (snapshot_name='snapshot name')")
                if snapshot_describe == None:
                    return HttpResponse("Must be to create a new snapshot is described (snapshot_describe='info')")
                result = vmaction.create_vm_snapshot(vm_instance, snapshot_name, snapshot_describe)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 69231, "errorDesc":"Create a snapshot failure"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "delete_specified_snapshot":
                if snapshot_name == None:
                    return HttpResponse("Must specify the snapshot name (snapshot_name='snapshot name')")
                result = vmaction.delete_vm_specified_snapshot(vm_instance, snapshot_name)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 98189, "errorDesc": "Delete snapshot failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "delete_current_snapshot":
                result = vmaction.delete_vm_current_snapshot(vm_instance)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 87652, "errorDesc":"Delete the current snapshot failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "get_snapshot_info":
                dt = vmaction.get_vm_snapshot_list(vm_instance)
                if dt == False or len(dt) == 0:
                    res = {"success": False, "data": "null", "errorCode": 76343, "errorDesc": "No snapshot"}
                    return HttpResponse(json.dumps(res))
                result = {"success": True, "data": dt, "errorCode": "null", "errorDesc": "null"}
                return HttpResponse(json.dumps(result))
            elif action_type == "vm_clone":
                if clone_vmname == None:
                    return HttpResponse("Formal parameters clone_vmname = 'clone name' must provide the name of the clone")
                result = vmaction.vm_clone(vm_instance, clone_vmname)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 21651, "errorDesc":"clone vm failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "vm_delete":
                Thread(target=vmaction.vm_delete, args=(vm_instance, )).start()
                info = {"success": True, "data": "Start delete vm", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(info))
            elif action_type == "add_disk":
                result = vmaction.vm_add_vdisk(vm_instance, datastore_name, vdisk_size)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 20011, "errorDesc":"add vdisk failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "chage_disk_size":
                result = vmaction.vm_chage_vdisk_size(vm_instance, vdisk_name, vdisk_size)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 65309, "errorDesc":"chage vdisk size failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "delete_vdisk":
                result = vmaction.vm_delete_vdisk(vm_instance, unit_number)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 674309, "errorDesc":"delete vdisk failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "chage_memory_size":
                result = vmaction.vm_chage_memory_size(vm_instance, memory_gb)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 78302, "errorDesc":"chage memory size failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "chage_cpu":
                result = vmaction.vm_chage_cpu(vm_instance, cpu_number, cpu_core)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 9983, "errorDesc":"chage cpu failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "chage_nic_conn":
                result = vmaction.vm_chage_nic_conn(vm_instance, nic_name, network_label)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 2103, "errorDesc":"chage nic conn failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "add_nic":
                result = vmaction.vm_add_nic(vm_instance, network_label)
                if result == False:
                    res = {"success": False, "data": "null", "errorCode": 2103, "errorDesc":"add nic failed"}
                    return HttpResponse(json.dumps(res))
                res = {"success": True, "data": "null", "errorCode": "null", "errorDesc":"null"}
                return HttpResponse(json.dumps(res))
            elif action_type == "vm_migration":
                result = vmaction.vm_migration(vm_instance, to_host)
                return HttpResponse(result)
            else:
                return HttpResponse("action of the unknown")
        else:
            return HttpResponse("Not allowed to get model")
    except Exception, e:
        return e

def create_vms(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            vmlist = data.get("vmlist", None)
            datastoreid = data.get("datastoreid", None)
            hostid = data.get("hostid", None)
            template_name = data.get("template_name", None)
            resourceid = data.get("resourceid", None)
            number = data.get("number", None)
            nameprefix = data.get("nameprefix", None)

            task_id = uuid.uuid4()
            task_str_ID = str(task_id)

            if vmlist != None:
                if isinstance(vmlist, list) != True:
                    error_info = {"success": False, "data": "null", "errorCode": 91121,"errorDesc": "Parameter: @vmlist, should be an array type"}
                    return HttpResponse(json.dumps(error_info))
                checkRepeat_Res = checkRepeat_VM_Name(vmlist)
                if len(checkRepeat_Res['repeatVMName']) != 0:
                    dt = {"success": False, "data": "null", "errorCode": 101121, "errorDesc": "discovery virtual machine name repetition, create stop"}
                    return HttpResponse(json.dumps(dt))
                else:
                    if len(checkRepeat_Res['availableVMName']) != 0:
                        create_vm_main(vmlist=vmlist, template_name=template_name, resourceid=resourceid, hostid=hostid, datastoreid=datastoreid, taskID=task_str_ID)
                        dt_n = {"taskID": task_str_ID}
                        dt = {"success": True, "data":dt_n, "errorCode": "null", "errorDesc": "null"}
                        return HttpResponse(json.dumps(dt))
                    else:
                        error_info = {"success": False, "data":"null", "errorCode":901267, "errorDesc":" vm creation fails"}
                        return HttpResponse(json.dumps(error_info))

            if number != None or nameprefix != None:
                new_vmname_list = []
                for i in range(number):
                    num = i + 1
                    new_vmname = "%s_%s" % (nameprefix, num)
                    new_vmname_list.append(new_vmname)
                checkRepeat_Res = checkRepeat_VM_Name(new_vmname_list)
                if len(checkRepeat_Res['repeatVMName']) != 0:
                    dt = {"success": False, "data": "null", "errorCode": 20110,"errorDesc": "discovery virtual machine name repetition, create stop"}
                    return HttpResponse(json.dumps(dt))
                else:
                    if len(checkRepeat_Res['availableVMName']) != 0:
                        available_vm_list = checkRepeat_Res['availableVMName']
                        create_vm_main(vmlist=available_vm_list, template_name=template_name, resourceid=resourceid,hostid=hostid, datastoreid=datastoreid, number=number, nameprefix=nameprefix,taskID=task_str_ID)
                        dt_n = {"taskID":task_str_ID}
                        dt = {"success": True, "data": dt_n, "errorCode": "null","errorDesc": "null"}
                        return HttpResponse(json.dumps(dt))
                    else:
                        error_info = {"success": False, "data": "null", "errorCode":221130,"errorDesc": "vm create fail"}
                        return HttpResponse(json.dumps(error_info))
        else:
            return HttpResponse("Not allowed to get model")
    except Exception, e:
        return e