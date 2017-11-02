#coding:utf-8
"""powershell数据处理"""

import codecs

def portGroup_Data():
    '''获取虚拟端口组数据'''
    portGroupList = []
    file = codecs.open("C:\VMware\\vc\src\powercli\psData\portGroup_Data.txt", "r", encoding="utf-16")
    data = file.readlines()
    for line in set(data): # set去重
        dt = line.replace("\r","").replace("\n","")
        portGroupList.append(dt)
    file.close()
    return portGroupList

