#coding:utf-8
"""The function of this program is to update the data with the powershell"""

from vc.src.db.table_ps_netlabel import emptData_from_table_ps_netlabel
from psScriptCall import callScript_get_port_group, callScript_get_datastorage_info

def update_netlabel():
    """Update network TAB"""
    emptData_from_table_ps_netlabel()  # Empty ps_netlabel
    result = callScript_get_port_group() # data is written to the database
    if result:
        print "Virtual Port Group data is successful"
        return True
    else:
        print "ERROR: Virtual Port Group data was fetched with an error"
        return False

def update_datastore_And_esxi_relation():
    """Update the correspondence between storage and ESXI"""
    result = callScript_get_datastorage_info() # data is written to the database
    if result == True:
        print "Datastore and esxi relationship data for success"
        return True
    else:
        print "ERROR: Error occurred when datastore and esxi relational data were obtained"
        return False

