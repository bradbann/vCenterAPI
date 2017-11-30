from pyVmomi import vim
from VMOmiConn import VMOmiConn

c = VMOmiConn()
s = c.startConn()

def get_resources_all_obj(vimtype=None):
    """Just by vimtype to get resource all object, return a list"""
    obj_list = []
    container = s.content.viewManager.CreateContainerView(
        s.content.rootFolder, vimtype, True)
    for c in container.view:
        obj_list.append(c)
    if obj_list:
        return obj_list
    else:
        print("Object of vimtype: {vimtypes} not found".format(vimtypes=vimtype))
        return obj_list

def getPortGroup():
    pglist = []
    netObjList = get_resources_all_obj(vimtype=[vim.Network])
    for netobj in netObjList:
        pglist.append(netobj.name)
    return pglist

def getDatastore():
    dstor_obj = get_resources_all_obj(vimtype=[vim.Datastore])
    dstor_list = []
    for dstor in dstor_obj:
        for host in dstor.host:
            hostname = host.key.name
        # The "Capacity" and "FreeSpace" units are bytes
        dstor_dict = {"Esxi": hostname,
                      "DatastoreName": dstor.name,
                      "Capacity": dstor.summary.capacity,
                      "FreeSpace": dstor.summary.freeSpace,
                      "DatastoreID": str(dstor.summary.datastore).split(":")[1].replace("'", "")
                      }
        dstor_list.append(dstor_dict)
    return dstor_list

def getResourcePool():
    rplist = []
    rObjList = get_resources_all_obj(vimtype=[vim.ResourcePool])
    for rpool in rObjList:
        rpdict = {"ResourceID": str(rpool.config.entity).split(":")[1].replace("'",""),
        "ResourceName": rpool.name
        }
        rplist.append(rpdict)
    return rplist
