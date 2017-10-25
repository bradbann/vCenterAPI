#coding:utf-8
from pysphere.resources import VimService_services as VI
from pysphere import VITask
from vc.src.conn_vcserver import ConnHelper

conn_obj = ConnHelper()
server = conn_obj.start_connect_server()

def change_memory_size(vminstance, memory_gb):
    '''修改虚拟机的内存大小'''
    memory_mb = memory_gb * 1024 #GB转换MB
    vm_obj = vminstance
    request = VI.ReconfigVM_TaskRequestMsg()
    _this = request.new__this(vm_obj._mor)
    _this.set_attribute_type(vm_obj._mor.get_attribute_type())
    request.set_element__this(_this)
    spec = request.new_spec()

    # 设置内存大小
    spec.set_element_memoryMB(memory_mb)

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
