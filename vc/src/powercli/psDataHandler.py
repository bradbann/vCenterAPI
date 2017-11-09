#coding:utf-8

from vc.src.db.table_ps_netlabel import emptData_from_table_ps_netlabel
from psScriptCall import callScript_get_port_group


def ps_netlabel_Handler():
    emptData_from_table_ps_netlabel()  # 清空表ps_netlabel
    result = callScript_get_port_group() # 获取数据并入库
    if result:
        print "Virtual Port Group数据获取成功"
        return True
    else:
        print "ERROR: Virtual Port Group数据获取时发生错误"
        return False
