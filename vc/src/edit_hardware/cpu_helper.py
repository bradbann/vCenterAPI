#coding:utf-8
from pysphere.resources import VimService_services as VI
from pysphere import VITask
from vc.src.conn_vcserver import ConnHelper

conn_obj = ConnHelper()
server = conn_obj.start_connect_server()

def change_cpu(vminstance=None, cpu_number=None, cpu_core=None):
    '''修改虚拟机CPU数量和核心数'''
    vm_obj = vminstance
    request = VI.ReconfigVM_TaskRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)
    spec = request.new_spec()

    if cpu_number is not None:
        spec.set_element_numCPUs(cpu_number)  # This sets CPU config to 2x1 (2个CPU分别为单核心)
    if cpu_core is not None:
        spec.set_element_numCoresPerSocket(cpu_core)  # This sets CPU config to 1x2 (instead of 2x2) 1个CPU双核

    request.set_element_spec(spec)
    ret = server._proxy.ReconfigVM_Task(request)._returnval
    task = VITask(ret, server)
    status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
    if status == task.STATE_SUCCESS:
        print "VM successfully reconfigured"
        return True
    elif status == task.STATE_ERROR:
        print "Error reconfiguring vm: %s" % task.get_error_message()
        return False
    server.disconnect()
