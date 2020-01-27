import re
import json

def SearchInVmxText(filepath,keyword):
    with open(filepath,'r') as fp:
        for line in fp:
            matchword = re.match(keyword,line)
            if matchword:
                return matchword.group(1)

def SearchInVmxTwoElements(filepath,keyword):
    with open(filepath,'r') as fp:
        for line in fp:
            list = re.findall(keyword,line)
            if list:
                return list

def SearchInVmx_AllDeviceNumber(filepath,keyword):
    with open(filepath,'r') as fp:
        list = []
        for line in fp:
            result = re.findall(keyword,line)
            if result:
                list.append(result[0])
        return list

def Vmx_displayName(filepath):
    keyword = r'displayName = "([a-zA-Z0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_virtualHWversion(filepath):
    keyword = r'virtualHW.version = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vCPU(filepath):
    keyword = r'numvcpus = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vMem(filepath):
    keyword = r'memSize = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_eth(filepath):
    eth_number = r'(ethernet[0-9]*).present = "TRUE"'
    eth_list = SearchInVmx_AllDeviceNumber(filepath,eth_number)

    for item in eth_list:
        element0 = item + r'.(virtualDev) = "(.*)"'
        element1 = item + r'.(networkName) = "(.*)"'
        list1 = SearchInVmxTwoElements(filepath,element0)
        list2 = SearchInVmxTwoElements(filepath,element1)
        dict1 = dict(list1)
        dict2 = dict(list2)
        dict1.update(dict2)
        dict3 = {item:dict1}
        print(dict3)
    
"""
def Vmx_scsi(filepath):
    keyword = r'scsi0:0.present = "(TRUE)"'
    return SearchInVmxText(filepath,keyword)
"""

def main():
    tmp_filepath = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/vmx/testVM.vmx'

    a = Vmx_virtualHWversion(tmp_filepath)
    b = Vmx_vCPU(tmp_filepath)
    c = Vmx_vMem(tmp_filepath)
    Vmx_eth(tmp_filepath)
    d = Vmx_displayName(tmp_filepath)
#    e = Vmx_scsi(tmp_filepath)

    print("VM name : " +d)
    print("HW version : " + a)
    print("vCPU : " + b)
    print("vMem : " + c)
 #   print("scsi : " + e)

    dict = {"VM name": d,"HW version": a,"vCPU": b,"vMem": c}
    json_file = open('../json/test.json', 'w')
    json.dump(dict, json_file)


main()
