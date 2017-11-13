# -*- coding: utf-8 -*-
from vc.src.vm_helper import VMInstance

class VM_Info(VMInstance):
    '''This class is used to obtain virtual machine information'''

    def get_vm_basic_info(self, vminstance):
        '''Vm common information'''
        try:
            data_total = []
            for vm in vminstance:
                # Get the disk information
                data = vm['obj']._disks
                disk_list = []
                for i in range(len(data)):
                    vdiskFile = data[i]["files"][0]["name"]
                    vdiskSize = data[i]["capacity"]  # 单位是KB
                    vdiskName = data[i]["label"]
                    vDiskunitNumber = data[i]["device"]["unitNumber"]
                    vdiskData = {"vDiskunitNumber":vDiskunitNumber,"vdiskFile": vdiskFile, "vdiskSize": vdiskSize, "vdiskName":vdiskName}
                    disk_list.append(vdiskData)

                #Get the network card information
                nic_list = []
                for dev in vm["obj"].properties.config.hardware.device:
                    if dev._type in ["VirtualVmxnet3", "VirtualE1000", "VirtualE1000e", "VirtualPCNet32", "VirtualVmxnet"]:  # 过滤有哪些适配器类型，如有新的类型，需在这里添加
                        nic_data = {"nicType": dev._type, "NetworkConnection": dev._obj.Backing.DeviceName,
                                    "nicName": dev._obj.DeviceInfo.Label, "mac": dev._obj.MacAddress,
                                    "WakeOnLanEnabled": dev._obj.WakeOnLanEnabled
                                    }
                        nic_list.append(nic_data)

                #Get the virtual machine snapshot information
                snapshots_list = []
                snapshots_instance = vm["obj"].get_snapshots()
                for snapshots_items in snapshots_instance:
                    time_data = snapshots_items.get_create_time()
                    new_time = "%s-%s-%s %s:%s:%s" % (time_data[0],time_data[1],time_data[2],time_data[3],time_data[4],time_data[5])
                    snapshots_data = {
                        "SnapshotsName": snapshots_items.get_name(),
                        "Description": snapshots_items.get_description(),
                        "CreatedTime": new_time,
                        "State": snapshots_items.get_state(),
                        "Path": snapshots_items.get_path(),
                        # "Parent":snapshots_items.get_parent(),
                        # "Children":snapshots_items.get_children()
                    }
                    snapshots_list.append(snapshots_data)

                vm_status = vm["obj"].get_status()
                esxi_host = vm["obj"].properties.runtime.host.name #Belonging to a physical machine
                vmIdent = vm['obj']._mor
                osType = vm['obj']._properties["guest_full_name"]
                memory_mb_size = vm['obj']._properties["memory_mb"]
                cpuNumber = vm['obj']._properties["num_cpu"]

                #Gets the virtual machine IP address
                vmip = None
                try:
                    vm["obj"].properties._flush_cache()
                    ip = vm["obj"].properties.guest.ipAddress
                    vmip = ip
                except AttributeError:
                    vmip = "null"

                #Summary data
                data_total.append({"osType":osType,
                                    "ip":vmip,
                                    "vmIdent":vmIdent,
                                    "name": vm["name"],
                                    "vmxfile": vm["path"],
                                    "state": vm_status,
                                    "esxi":esxi_host,
                                    "virtualdisk":disk_list,
                                    "memorySize":memory_mb_size,
                                    "cpuNumber":cpuNumber,
                                    "NIC":nic_list,
                                    "snapshots": snapshots_list
                                    })
            return data_total
        except Exception, e:
            print e
            return False