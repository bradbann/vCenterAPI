#coding:utf-8
"""此程序的作用是通过powershell去更新数据的操作"""

from vc.src.db.table_ps_netlabel import emptData_from_table_ps_netlabel
from psScriptCall import callScript_get_port_group, callScript_get_datastorage_info


def update_netlabel():
    """更新网络标签"""
    emptData_from_table_ps_netlabel()  # 清空表ps_netlabel
    result = callScript_get_port_group() # 获取数据并入库
    if result:
        print "Virtual Port Group数据获取成功"
        return True
    else:
        print "ERROR: Virtual Port Group数据获取时发生错误"
        return False

def update_datastore_And_esxi_relation():
    """更新存储和ESXI的对应关系"""
    result = callScript_get_datastorage_info() # 获取数据并入库
    if result == True:
        print "datastore和esxi关系数据获取成功"
        return True
    else:
        print "ERROR: datastore和esxi关系数据获取时发生错误"
        return False

