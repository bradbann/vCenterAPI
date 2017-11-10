#coding:utf-8
import cPickle as pickle
from vc.src.vm_helper import VMInstance
from vc.src.vmExistChecked import vmListExistChecked
from vc.src.device_info.vm_info import VM_Info
from vc.src.conf import DTFile

from db import table_urun_task_id

vminstance = VMInstance()
vminfo = VM_Info()

def all_get_vmCreate_status():
    '''查询创建记录，该函数用于后台使用'''
    try:
        pkl_file = open(DTFile, 'rb')
    except IOError:
        error_info = {"success": False, "data": "null", "errorCode": 23412, "errorDesc": "database has no data"}
        return error_info
    while True:
        try:
            data = pickle.load(pkl_file)
            print data
        except EOFError:
            pkl_file.close()
            break

def ipCheck(vmlist):
    '''通过检查虚拟机是否存在IP地址来判断是否部署成功，并将部署成功的虚拟机以列表的形式返回'''
    also_is_createList = []         #存储还在创建的虚拟机
    vmExistList = []            #存储虚拟机是否存在（作为临时存储用）
    create_doneList = []        #存储有IP地址的虚拟机
    vmCheckRes = vmListExistChecked(vmlist)         #判断检查结果
    if len(vmCheckRes['notExist']) != 0:
        for vm in vmCheckRes['notExist']:
            also_is_createList.append(vm["vmname"])
    if len(vmCheckRes["exist"]) != 0:
        vmExistList = vmCheckRes["exist"]
    vmObjList = vminstance.get_aGroupVMInstance(vmExistList)
    for vm in vmObjList:
        try:
            vm["obj"].properties._flush_cache()
            ip = vm["obj"].properties.guest.ipAddress
            if ip:
                create_doneList.append(vm["name"])
        except Exception:
            also_is_createList.append(vm["name"])
    dt = {"alsoCreate":also_is_createList, "createDone":create_doneList}
    return dt

def get_vmCreate_status(taskID):
    '''通过任务ID查询虚拟机的信息'''
    # try:
    #     pkl_file = open(DTFile, 'rb')
    # except Exception:
    #     error_info = {"success": False, "data": "null", "errorCode": 23412, "errorDesc": "database has no data"}
    #     return error_info
    # res = None
    # while True:
    #     try:
    #         data = pickle.load(pkl_file)
    #         if data.has_key(taskID):
    #             res = data.get(taskID, None)
    #         else:pass
    #     except EOFError:
    #         break
    res = table_urun_task_id.readData_from_table_urunTaskID(taskID) #从数据库中读取taskid
    if res:
        vmlist = res
        ipCheckResult = ipCheck(vmlist) #这里调用虚拟机的创建状态，通过获取到IP地址并是否能Ping通来判断部署成功与否
        if len(ipCheckResult['createDone']) == 0:
            #如果createDone列表完全没有可用的虚拟机则告知用户虚拟机还在创建
            error_info = {"success": 1, "data":"null", "errorCode":"null", "errorDesc":"vm is still in create, please try again lster"}
            return error_info
        ins_list = vminstance.get_aGroupVMInstance(ipCheckResult['createDone'])
        dt = vminfo.get_vm_basic_info(ins_list)
        if len(dt) == 0: #如果存放的数据列表为空，表示没有虚拟机数据
            not_data = {"success": False, "data":"null", "errorCode":112233, "errorDesc":"no data"}
            return not_data
        else:
            dataTotal = {"isCreate":ipCheckResult["alsoCreate"], "createDone":dt}
            res = {"success": True, "data": dataTotal, "errorCode":"null", "errorDesc":"null"}
            return res
    else:
        error_info = {"success": False, "data": "null", "errorCode": 992200, "errorDesc": "task ID is not found"}
        return error_info

#print get_vmCreate_status('4d140a9d-52d8-4da6-8ba4-2026ae089052')
#all_get_vmCreate_status()