from pysphere import VIProperty
from conn_vcserver import ConnHelper

class PhysicalHost(ConnHelper):

    def __init__(self):
        super(PhysicalHost, self).__init__()
        super(PhysicalHost, self).start_connect_server()

    def get_host_info(self):
        hosts = self.server.get_hosts()
        for host in hosts:
            p = VIProperty(self.server, host)
            overallCpuUsage = p.summary.quickStats.overallCpuUsage
            overallMemoryUsage = p.summary.quickStats.overallMemoryUsage
            averagedCpuSpeedPerCore = p.hardware.cpuInfo.hz
            numCpuCores = p.hardware.cpuInfo.numCpuCores
            totalCpuSpeed = averagedCpuSpeedPerCore * numCpuCores
            totalMemorySize = p.hardware.memorySize
            uptime = p.summary.quickStats.uptime
            uptime = uptime * 100

            print "Host:%s | IP:%s | CpuUsage=%s MemoryUsage=%s" % (str(hosts.keys()[0]), str(hosts.values()[0]), str(overallCpuUsage), str(overallMemoryUsage))

if __name__ == '__main__':

    pass