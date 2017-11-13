# -*- coding: utf-8 -*-

class From_Template_Clone_VM:
    '''Deploy the virtual machine from the template'''
    def __get_rp(self, s,rp):
        '''Check that the resource pool exists
        @rp: Resource pool id
        '''
        rps_list = s.get_resource_pools().keys()
        if rp in rps_list:
            index = rps_list.index(rp)
            dd = rps_list[index]
            return dd
        else:
            print "Resource pool does not exist"
            return None

    def __get_dt(self, s, dtname):
        '''Check if the datastore exists
        @dtname: datastore id
        '''
        dts_list = s.get_datastores().keys()
        if dtname in dts_list:
            index = dts_list.index(dtname)
            dd = dts_list[index]
            return dd
        else:
            print "datastores does not exist"
            return None

    def __get_host(self, s, hname):
        '''Check that the host is present
        @hname: esxi id
        '''
        esxi_list = s.get_hosts().keys()
        if hname in esxi_list:
            index = esxi_list.index(hname)
            dd = esxi_list[index]
            return dd
        else:
            print "host does not exist"
            return None

    def start_fromTemplate_cloneVM(self, s, name, template_name, pool, esx, lun):
        '''This is the main tuning, note: the resource pool resgroup-37 is available and is passed in'''
        template = s.get_vm_by_name(template_name)
        template.clone(name, host=self.__get_host(s, esx), resourcepool=self.__get_rp(s, pool), datastore=self.__get_dt(s, lun), sync_run=False)
