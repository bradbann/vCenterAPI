#-*- coding: utf-8 -*-
"""
这个模块是关于虚拟机的操作
"""
from pysphere.resources import VimService_services as VI
from pysphere.vi_task import VITask
from conn_vcserver import ConnHelper
from create_vm import From_Template_Clone_VM
from vc.src.edit_hardware.vdisk_helper import VDisk
from vc.src.edit_hardware.memory_helper import change_memory_size
from vc.src.edit_hardware.cpu_helper import change_cpu
from vc.src.edit_hardware.nic_helper import NIC

# 实例化
vdisk = VDisk()
nic = NIC()

class VMInstance(ConnHelper):
    """
    这个类的主要作用是生成虚拟机实例，并保存到列表
    """
    def __init__(self):
        """初始化父类
        实例化VMInstance类的实例时，就已经调用了父类中的start_connect_server方法
        """
        super(VMInstance,self).__init__()
        super(VMInstance, self).start_connect_server()

    def get_filter_vm(self, state_type, datacenter=None, cluster=None, resource_pool=None):
        """这个方法的作用是根据电源状态;集群名字;数据中心名字得到一个虚拟机路径放在列表并作为参数传给get_vminstance_by_path方法
        从而来得到虚拟机的实例。
        parameter:
            param 这个参数是必须的,通过电源状态获取虚拟机，默认是'ALL'获取所有, 状态:'POWER_ON', 'POWER_OFF', 'SUSPENDED'
            datacenter 通过数据中心过滤
            cluster 通过集群过滤
            resource_pool 通过资源池过滤
        """
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
        """这个方法的主要作用是根据虚拟机路径得到一个虚拟机实例对象
        通常由get_filter_vm方法处理后将虚拟机路径列表传到这个方法
        也可以单独使用这个方法，单独使用时传入的值应为字符串类型的虚拟机路径信息
        参数：
            vmpath: 虚拟机路径
        """
        try:
            vm_instance_list = [] #虚拟机名字
            if isinstance(vmpath, list): #判断是否为列表类型，如果是则由get_filter_vm方法处理传过来的值。如果不是则是单独使用该方法
                for i in range(len(vmpath)):
                    vminstance = self.server.get_vm_by_path(vmpath[i])
                    vmname = vminstance.get_properties()["name"]
                    vminstancedict = {"name":vmname, "obj":vminstance,"path":vmpath[i]}
                    vm_instance_list.append(vminstancedict)
                return vm_instance_list
            else:
                #单独使用该方法
                vminstance = self.server.get_vm_by_path(vmpath)
                vmname = vminstance.get_properties()["name"]
                vminstancedict = {"name": vmname, "obj": vminstance,"path":vmpath}
                vm_instance_list.append(vminstancedict)
                return vm_instance_list
        except Exception, e:
            print e
            return None

    def get_vm_instance_by_name(self, vmname):
        """这个方法的主要作用通过虚拟机名字来得到一个虚拟机实例对象
        参数:
            vmname:
        """
        try:
            vm_instance_list = []
            vminstance = self.server.get_vm_by_name(vmname)
            vmpath = vminstance.get_properties()["path"]
            vminstancedict = {"name":vmname, "obj": vminstance, "path":vmpath}
            vm_instance_list.append(vminstancedict)
            return vm_instance_list #返回虚拟机实例列表
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
            return vminstance_list #如果返回的是空列表，原因是要么没有这个虚拟机，要么还正在部署中

class VMAction(VMInstance):
    """这个类的主要是针对实例的操作，如获取的属性、开关机迁移功能"""
    def vm_power_on(self, vminstance):
        '''虚拟机开机
        参数:
            vminstance: 虚拟机实例
        '''
        try:
            for vm in vminstance:
                if vm["obj"].is_powered_on():pass
                else:vm["obj"].power_on(sync_run=False)
            return True
        except Exception, e:
            return False

    def vm_power_off(self, vminstance):
        '''虚拟机关机
        参数:
            vminstance: 虚拟机实例
        '''
        try:
            for vm in vminstance:
                if vm["obj"].is_powered_off():pass
                else:vm["obj"].power_off(sync_run=False)
            return True
        except Exception, e:
            return False

    def vm_reset(self, vminstance):
        '''虚拟机重启
        参数:
            vminstance: 虚拟机实例
            '''
        try:
            for vm in vminstance:
                vm["obj"].reset()
            return True
        except Exception, e:
            return False

    def vm_power_suspend(self, vminstance):
        '''虚拟机暂停
        参数:
            vminstance: 虚拟机实例
        '''
        try:
            for vm in vminstance:
                vm["obj"].suspend(sync_run=False)
            return True
        except Exception, e:
            return False

    def revert_vm_current_snapshot(self, vminstance):
        '''恢复当前快照
        参数:
            vminstance: 虚拟机实例
        '''
        try:
            for vm in vminstance:
                vm["obj"].revert_to_snapshot(sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def revert_vm_specified_snapshot(self, vminstance, snapshot_name):
        '''恢复指定快照
        参数:
            vminstance: 虚拟机实例
            snapshot_name: 快照名称
        '''
        try:
            for vm in vminstance:
                vm["obj"].revert_to_named_snapshot(snapshot_name, sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def create_vm_snapshot(self, vminstance, snapshot_name, description):
        '''创建快照
        参数：
            vminstance：虚拟机实例
            snapshot_name,：创建快照的快照名称
            description：对快照的描述
        '''
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
        '''删除指定名称快照
        参数：
            vminstance：虚拟机实例
            snapshot_name:需删除的快照名称
        '''
        try:
            for vm in vminstance:
                vm["obj"].delete_named_snapshot(snapshot_name, sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def delete_vm_current_snapshot(self, vminstance):
        '''删除当前快照
        参数：
            vminstance：虚拟机实例
        '''
        try:
            for vm in vminstance:
                vm["obj"].delete_current_snapshot(sync_run=False)
            return True
        except Exception,e:
            print e
            return False

    def get_vm_snapshot_list(self, vminstance):
        '''获取虚拟机实例的快照信息
        参数：
            vminstance：虚拟机实例
        '''
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
        '''对指定的虚拟机进行克隆
        @vminstance: 虚拟机实例
        @clone_name：克隆虚拟机新的名称'''
        try:
            for vm in vminstance:
                vm["obj"].clone(clone_vmname, sync_run=False, power_on=False)
            return True
        except Exception,e:
            return False

    def vm_migration(self, vminstance, to_host):
        '''迁移虚拟机（此功能是需有共享存储的架构）
        参数：
            vminstance: 虚拟机实例
            to_host: 模板ESXI主机
        '''
        try:
            for vm in vminstance:
                vm['obj'].migrate(host=to_host)
            return True
        except Exception,e:
            print e
            return False


    def vm_delete(self, vminstance):
        '''从磁盘中删除虚拟机
        参数：
            vminstance: 虚拟机实例
        '''
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
        '''从模板创建虚拟机
        参数：
            name: 虚拟机名称
            template_name： 模板名称
            pool： 资源池
            esx： ESX主机
            lun： datastore
        '''
        try:
            s = self.start_connect_server() #连接对象实例
            objCloneVM = From_Template_Clone_VM()
            objCloneVM.start_fromTemplate_cloneVM(s, name, template_name, pool, esx, lun)
            return True
        except Exception, e:
            return False

    def vm_add_vdisk(self, vminstance, datastore_name, vdisk_size_gb):
        '''虚拟机添加磁盘
        参数：
            vminstance： 虚拟机实例
            datastore_name： datastore（lun）名称，创建的虚拟磁盘存放到哪个lun
            vdisk_size_gb： 虚拟磁盘容量大小
        '''
        try:
            for vm in vminstance:
                vdisk.add_vdisk(vm['obj'], datastore_name, vdisk_size_gb)
            return True
        except Exception, e:
            print e
            return False

    def vm_chage_vdisk_size(self, vminstance, vdisk_name, vdisk_size):
        '''虚拟机指定的虚拟磁盘的容量大小
        参数：
            vminstance: 虚拟机实例
            vdisk_name: 虚拟硬盘名称
            vdisk_size: 容量大小
        '''
        try:
            for vm in vminstance:
                vdisk.change_vdisk_size(vm['obj'], vdisk_name, vdisk_size)
            return True
        except Exception, e:
            print e
            return False

    def vm_delete_vdisk(self, vminstance, unit_number):
        '''删除虚拟机的虚拟硬盘
        参数：
            vminstance： 虚拟机实例
            unit_number: 虚拟硬盘节点单元号
        '''
        try:
            for vm in vminstance:
                vdisk.delete_vdisk_size(vm['obj'], unit_number)
            return True
        except Exception,e:
            print e
            return False

    def vm_chage_memory_size(self, vminstance, memory_gb):
        '''修改虚拟机的内存大小
        参数：
            vminstance：VM实例
            memory_gb： memory大小
        '''
        try:
            for vm in vminstance:
                change_memory_size(vm['obj'], memory_gb)
            return True
        except Exception,e:
            print e
            return False

    def vm_chage_cpu(self, vminstance, cpu_number=None, cpu_core=None):
        '''修改虚拟机CPU数量和核心数量
        参数：
            vminstance: VM实例
            cpu_number: CPU数量
            cpu_core: CPU核心数量
        '''
        try:
            for vm in vminstance:
                change_cpu(vm['obj'], cpu_number, cpu_core)
            return True
        except Exception,e:
            print e
            return False

    def vm_chage_nic_conn(self, vminstance, nic_name, network_label):
        '''修改虚拟机指定网卡连接到指定网络标签
        参数：
            vminstance: 虚拟机实例
            nic_name: 网卡名称
            network_label: 网络标签
        '''
        try:
            for vm in vminstance:
                nic.nic_chage_conn(vm['obj'], nic_name, network_label)
            return True
        except Exception,e:
            print e
            return False

    def vm_add_nic(self, vminstance, network_label):
        '''给指定的虚拟机添加网卡后并连接到指定的网络标签
        参数：
            vminstance: VM实例
            network_label: 网络标签
        '''
        try:
            for vm in vminstance:
                nic.add_nic(vm['obj'], network_label)
            return True
        except Exception,e:
            print e
            return False






