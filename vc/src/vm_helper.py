#-*- coding: utf-8 -*-
"""This module is about the operation of the virtual machine"""

from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask
from conn_vcserver import ConnHelper
from create_vm import From_Template_Clone_VM
from vc.src.edit_hardware.vdisk_helper import VDisk
from vc.src.edit_hardware.memory_helper import change_memory_size
from vc.src.edit_hardware.cpu_helper import change_cpu
from vc.src.edit_hardware.nic_helper import NIC

vdisk = VDisk()
nic = NIC()

class VMInstance(ConnHelper):
    def __init__(self):
        super(VMInstance,self).__init__()
        super(VMInstance, self).start_connect_server()

    def get_filter_vm(self, state_type, datacenter=None, cluster=None, resource_pool=None):
        if state_type not in ['ALL', 'POWER_ON', 'POWER_OFF', 'SUSPENDED']:
            return False
        if state_type == 'ALL':
            result = self.get_vm_instance_by_path(self.server.get_registered_vms(datacenter, cluster, resource_pool))
            return result
        elif state_type == 'POWER_ON':
            result = self.get_vm_instance_by_path(self.server.get_registered_vms(datacenter, cluster, resource_pool, status='poweredOn'))
            return result
        elif state_type == 'POWER_OFF':
            result = self.get_vm_instance_by_path(self.server.get_registered_vms(datacenter, cluster, resource_pool, status='poweredOff'))
            return result
        elif state_type == 'SUSPENDED':
            result = self.get_vm_instance_by_path(self.server.get_registered_vms(datacenter, cluster, resource_pool, status='suspended'))
            return result
        else:
            return None

    def get_vm_instance_by_path(self,vmpath):
        try:
            vm_instance_list = []
            if isinstance(vmpath, list):
                for i in range(len(vmpath)):
                    vminstance = self.server.get_vm_by_path(vmpath[i])
                    vmname = vminstance.get_properties()["name"]
                    vminstancedict = {"name":vmname, "obj":vminstance,"path":vmpath[i]}
                    vm_instance_list.append(vminstancedict)
                return vm_instance_list
            else:
                vminstance = self.server.get_vm_by_path(vmpath)
                vmname = vminstance.get_properties()["name"]
                vminstancedict = {"name": vmname, "obj": vminstance,"path":vmpath}
                vm_instance_list.append(vminstancedict)
                return vm_instance_list
        except Exception, e:
            print e
            return None

    def get_vm_instance_by_name(self, vmname):
        try:
            vm_instance_list = []
            vminstance = self.server.get_vm_by_name(vmname)
            vmpath = vminstance.get_properties()["path"]
            vminstancedict = {"name":vmname, "obj": vminstance, "path":vmpath}
            vm_instance_list.append(vminstancedict)
            return vm_instance_list
        except Exception, e:
            print e
            return None

    def get_aGroupVMInstance(self, *args):
        vminstance_list = []
        try:
            for vm in args[0]:
                dt = self.get_vm_instance_by_name(vm)
                vminstance_list.append(dt[0])
            return vminstance_list
        except TypeError:
            return vminstance_list

class VMAction(VMInstance):
    """The main object of this class is the operation of the instance, such as the acquired property,
    the switch machine migration function"""
    def vm_power_on(self, vminstance):
        try:
            for vm in vminstance:
                if vm["obj"].is_powered_on():pass
                else:vm["obj"].power_on(sync_run=False)
            return True
        except Exception, e:
            return False

    def vm_power_off(self, vminstance):
        try:
            for vm in vminstance:
                if vm["obj"].is_powered_off():pass
                else:vm["obj"].power_off(sync_run=False)
            return True
        except Exception, e:
            return False

    def vm_reset(self, vminstance):
        try:
            for vm in vminstance:
                vm["obj"].reset()
            return True
        except Exception, e:
            return False

    def vm_power_suspend(self, vminstance):
        try:
            for vm in vminstance:
                vm["obj"].suspend(sync_run=False)
            return True
        except Exception, e:
            return False

    def revert_vm_current_snapshot(self, vminstance):
        try:
            for vm in vminstance:
                vm["obj"].revert_to_snapshot(sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def revert_vm_specified_snapshot(self, vminstance, snapshot_name):
        try:
            for vm in vminstance:
                vm["obj"].revert_to_named_snapshot(snapshot_name, sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def create_vm_snapshot(self, vminstance, snapshot_name, description):
        try:
            for vm in vminstance:
                vm_status = vm["obj"].get_status()
                if vm_status == "POWERED ON":
                    vm["obj"].create_snapshot(snapshot_name, description=description, memory=False, quiesce=True, sync_run=False)
                else:
                    vm["obj"].create_snapshot(snapshot_name, description=description, sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def delete_vm_specified_snapshot(self, vminstance, snapshot_name):
        try:
            for vm in vminstance:
                vm["obj"].delete_named_snapshot(snapshot_name, sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def delete_vm_current_snapshot(self, vminstance):
        try:
            for vm in vminstance:
                vm["obj"].delete_current_snapshot(sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def get_vm_snapshot_list(self, vminstance):
        try:
            snapshots_list = []
            for vm in vminstance:
                snapshots_instance = vm["obj"].get_snapshots()
                for snapshots_items in snapshots_instance:
                    time_data = snapshots_items.get_create_time()
                    new_time = "%s-%s-%s %s:%s:%s" % (time_data[0],time_data[1],time_data[2],time_data[3],time_data[4],time_data[5])
                    snapshots_data = {
                        "SnapshotsName":snapshots_items.get_name(),
                        "Description":snapshots_items.get_description(),
                        "CreatedTime":new_time,
                        "State":snapshots_items.get_state(),
                        "Path":snapshots_items.get_path(),
                        #"Parent":snapshots_items.get_parent(),
                        #"Children":snapshots_items.get_children()
                    }
                    snapshots_list.append(snapshots_data)
            return snapshots_list
        except Exception,e:
            print e
            return False

    def vm_clone(self, vminstance, clone_vmname):
        try:
            for vm in vminstance:
                vm["obj"].clone(clone_vmname, sync_run=False, power_on=False)
            return True
        except Exception,e:
            return False

    def vm_migration(self, vminstance, to_host):
        try:
            for vm in vminstance:
                vm['obj'].migrate(host=to_host)
            return True
        except Exception,e:
            print e
            return False


    def vm_delete(self, vminstance):
        try:
            for vms in vminstance:
                vm = vms["obj"]
                if vm.is_powered_on():vm.power_off(sync_run=False)
                # Invoke Destroy_Task
                request = VI.Destroy_TaskRequestMsg()
                _this = request.new__this(vm._mor)
                _this.set_attribute_type(vm._mor.get_attribute_type())
                request.set_element__this(_this)
                ret = self.server._proxy.Destroy_Task(request)._returnval
                # Wait for the task to finish
                task = VITask(ret, self.server)
                status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
                #if status == task.STATE_SUCCESS:
                 #   return True
                #elif status == task.STATE_ERROR:
                 #   print "Error removing vm:", task.get_error_message()
                  #  return False
            return True
        except Exception,e:
            return False

    def vm_from_template_create(self, name=None, template_name=None, pool=None, esx=None, lun=None):
        try:
            s = self.start_connect_server()
            objCloneVM = From_Template_Clone_VM()
            objCloneVM.start_fromTemplate_cloneVM(s, name, template_name, pool, esx, lun)
            return True
        except Exception, e:
            return False

    def vm_add_vdisk(self, vminstance, datastore_name, vdisk_size_gb):
        try:
            for vm in vminstance:
                vdisk.add_vdisk(vm['obj'], datastore_name, vdisk_size_gb)
            return True
        except Exception, e:
            print e
            return False

    def vm_chage_vdisk_size(self, vminstance, vdisk_name, vdisk_size):
        try:
            for vm in vminstance:
                vdisk.change_vdisk_size(vm['obj'], vdisk_name, vdisk_size)
            return True
        except Exception, e:
            print e
            return False

    def vm_delete_vdisk(self, vminstance, unit_number):
        try:
            for vm in vminstance:
                vdisk.delete_vdisk(vm['obj'], unit_number)
            return True
        except Exception,e:
            print e
            return False

    def vm_chage_memory_size(self, vminstance, memory_gb):
        try:
            for vm in vminstance:
                change_memory_size(vm['obj'], memory_gb)
            return True
        except Exception,e:
            print e
            return False

    def vm_chage_cpu(self, vminstance, cpu_number=None, cpu_core=None):
        try:
            for vm in vminstance:
                change_cpu(vm['obj'], cpu_number, cpu_core)
            return True
        except Exception,e:
            print e
            return False

    def vm_chage_nic_conn(self, vminstance, nic_name, network_label):
        try:
            for vm in vminstance:
                nic.nic_chage_conn(vm['obj'], nic_name, network_label)
            return True
        except Exception,e:
            print e
            return False

    def vm_add_nic(self, vminstance, network_label):
        try:
            for vm in vminstance:
                nic.add_nic(vm['obj'], network_label)
            return True
        except Exception,e:
            print e
            return False






