# -*- coding: utf-8 -*-

class From_Template_Clone_VM:
    '''从模板部署虚拟机'''
    def __get_rp(self, s,rp):
        '''检查资源池是否存在
        @rp: 资源池id'''
        rps_list = s.get_resource_pools().keys()
        if rp in rps_list:
            index = rps_list.index(rp)
            dd = rps_list[index]
            return dd
        else:
            print "Resource pool does not exist"
            return None

    def __get_dt(self, s, dtname):
        '''检查datastore是否存在
        @dtname: datastore id'''
        dts_list = s.get_datastores().keys()
        if dtname in dts_list:
            index = dts_list.index(dtname)
            dd = dts_list[index]
            return dd
        else:
            print "datastores does not exist"
            return None

    def __get_host(self, s, hname):
        '''检查主机是否存在
        @hname: esxi id'''
        esxi_list = s.get_hosts().keys()
        if hname in esxi_list:
            index = esxi_list.index(hname)
            dd = esxi_list[index]
            return dd
        else:
            print "host does not exist"
            return None

    def start_fromTemplate_cloneVM(self, s, name, template_name, pool, esx, lun):
        '''这是主调用，注意：资源池resgroup-37是可用的，传入这个即可'''
        template = s.get_vm_by_name(template_name)
        template.clone(name, host=self.__get_host(s, esx), resourcepool=self.__get_rp(s, pool), datastore=self.__get_dt(s, lun), sync_run=False)
