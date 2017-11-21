from VMOmiConn import VMOmiConn

c = VMOmiConn()
server = c.startConn()
datacenter = server.content.rootFolder.childEntity

def getPortGroup():
    pglist = []
    for item in datacenter:
        for pg in item.networkFolder.childEntity:
            pglist.append(pg.name)
    return pglist

def getDatastore():
    dstorelist = []
    for item in datacenter:
        for lun in item.datastoreFolder.childEntity:
            for lunObj in lun.childEntity:
                host = None
                for hostObj in lunObj.host:
                    host = hostObj.key.name
                dtDict = {
                    "Esxi": host,
                    "FreeSpace": lunObj.summary.freeSpace,
                    "DatastoreName": lunObj.summary.name,
                    "Capacity": lunObj.summary.capacity,
                    "DatastoreID": str(lunObj.summary.datastore).split(":")[1].replace("'","")
                }
                dstorelist.append(dtDict)
    return dstorelist

def getResourcePool():
    rlist = []
    for item in datacenter:
        for rpool in item.hostFolder.childEntity:
            dt = rpool.resourcePool
            rlist.append({
                "ResourceID":str(dt.config.entity).split(":")[1].replace("'",""),
                "ResourceName":dt.name
            })
    return rlist
