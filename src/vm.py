import os
import re
import json
import xml.etree.ElementTree as et
import argparse

def SearchInVmxText(filepath,keyword):
    with open(filepath,'r') as fp:
        for line in fp:
            matchword = re.match(keyword,line)
            if matchword:
                return matchword.group(1)

def SearchInVmx_AllDeviceNumber(filepath,keyword):
    with open(filepath,'r') as fp:
        list = []
        for line in fp:
            result = re.findall(keyword,line)
            if result:
                list.append(result[0])
        return list

def Vmx_displayName(filepath):
    keyword = r'displayName = "(.*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_virtualHWversion(filepath):
    keyword = r'virtualHW.version = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vCPU(filepath):
    keyword = r'numvcpus = "([0-9]*)"'
    Num_vCPU = SearchInVmxText(filepath,keyword)
    if Num_vCPU == None:
        Num_vCPU = 1
    return Num_vCPU

def Vmx_vMem(filepath):
    keyword = r'memSize = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vNIC(filepath):
    eth_number = r'(ethernet[0-9]*).present = "TRUE"'
    eth_list = SearchInVmx_AllDeviceNumber(filepath,eth_number) # <---- need vNIC number test

    list = []

    for item in eth_list:
        element = item + r'.virtualDev = "(.*)"'
        Device = SearchInVmxText(filepath,element)

        element = item + r'.networkName = "(.*)"'
        PortgroupName = SearchInVmxText(filepath,element)

        list.append({"Content":item + r'.virtualDev',"Detail":Device})
        list.append({"Content":item + r'.networkName',"Detail":PortgroupName})

    return(list)

def Vmx_vDisk(filepath):
    vDisk_number = r'(scsi[0-9]*:[0-9]*).present = "TRUE"'
    vDisk_list = SearchInVmx_AllDeviceNumber(filepath,vDisk_number) # <---- need scsi number test

    list = []

    for item in vDisk_list:
        element = item + r'.fileName = "(.*)"'
        vDiskName = SearchInVmxText(filepath,element)

        list.append({"Content":item + r'.fileName',"Detail":vDiskName})

    return(list)

def Vmx_vBus(filepath):
    vBus_number = r'(scsi[0-9]*).present = "TRUE"'
    vBus_list = SearchInVmx_AllDeviceNumber(filepath,vBus_number)

    list = []

    for item in vBus_list:
        element = item + r'.virtualDev = "(.*)"'
        vBusName = SearchInVmxText(filepath,element)

        list.append({"Content":item + r'.virtualDev',"Detail":vBusName})

    return(list)

def ShowVMList(path):
    target_path = os.path.join(path,"etc","vmware","hostd","vmInventory.xml")
    tree = et.parse(target_path)
    root = tree.getroot()
    list = []
    for name in root.iter('vmxCfgPath'):
        list.append(name.text)
    
    return(list)

def main():
    vmsupport_filepath = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/test-vm_support1'
    """
    parser = argparse.ArgumentParser(prog='vm.py',usage='Summarize VM Information',description='description',epilog='end',add_help=True)
    parser.add_argument('-f', '--file',help='input the vm-support directory',type=str,required=True)
    args = parser.parse_args()
    vmsupport_filepath = args.file
    """
    VMXpaths = ShowVMList(vmsupport_filepath)
    for VMXpath in VMXpaths:
        vmsupport_VMXpath = vmsupport_filepath + VMXpath
        list = []
        list = [
            {
                "Content":"VM name",
                "Detail":Vmx_displayName(vmsupport_VMXpath)
            },
            {
                "Content":"VM Hardware version",
                "Detail":Vmx_virtualHWversion(vmsupport_VMXpath)
            },
            {
                "Content":"vCPU",
                "Detail":Vmx_vCPU(vmsupport_VMXpath)
            },
            {
                "Content":"vMem",
                "Detail":Vmx_vMem(vmsupport_VMXpath)
            }
        ]

        vNICList = Vmx_vNIC(vmsupport_VMXpath)
        list.extend(vNICList)

        vDiskList = Vmx_vDisk(vmsupport_VMXpath)
        list.extend(vDiskList)

        vBusList = Vmx_vBus(vmsupport_VMXpath)
        list.extend(vBusList)

        dict = {}
        dict = {
            "format":{
                "title": "VM Information",
                "labels":[
                    {"name":"Content" ,"type":"text"},
                    {"name":"Detail"  ,"type":"text"}
                ],
                "hasHeader": True,
                "hasIndex": True
            },
            "data":list
        }

        VMXname = os.path.splitext(os.path.basename(vmsupport_VMXpath))[0]
        json_file = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','VM',VMXname + '.json'), 'w')
        json.dump(dict, json_file,indent=4)
        #print(json.dumps(dict, json_file,indent=4))

main()
