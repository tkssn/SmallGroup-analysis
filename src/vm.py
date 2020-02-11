import re
import json

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

def Vmx_vNIC(filepath):
    eth_number = r'(ethernet[0-9]*).present = "TRUE"'
    eth_list = SearchInVmx_AllDeviceNumber(filepath,eth_number) # <---- need vNIC number test

    dict = {}
    list = []

    for item in eth_list:
        element = item + r'.virtualDev = "(.*)"'
        Device = SearchInVmxText(filepath,element)

        element = item + r'.networkName = "(.*)"'
        PortgroupName = SearchInVmxText(filepath,element)

        dict[item + r'.virtualDev']  = Device
        dict[item + r'.networkName'] = PortgroupName

        list.append({"name":item + r'.virtualDev',"type":"text"})
        list.append({"name":item + r'.networkName',"type":"text"})

    return(dict,list)

def Vmx_vDisk(filepath):
    vDisk_number = r'(scsi[0-9]*:[0-9]*).present = "TRUE"'
    vDisk_list = SearchInVmx_AllDeviceNumber(filepath,vDisk_number) # <---- need scsi number test

    dict = {}
    list = []

    for item in vDisk_list:
        element = item + r'.fileName = "(.*)"'
        vDiskName = SearchInVmxText(filepath,element)

        dict[item + r'.fileName']  = vDiskName

        list.append({"name":item + r'.fileName',"type":"text"})

    return(dict,list)

def Vmx_vBus(filepath):
    vBus_number = r'(scsi[0-9]*).present = "TRUE"'
    vBus_list = SearchInVmx_AllDeviceNumber(filepath,vBus_number)

    dict = {}
    list = []

    for item in vBus_list:
        element = item + r'.virtualDev = "(.*)"'
        vBusName = SearchInVmxText(filepath,element)

        dict[item + r'.virtualDev']  = vBusName

        list.append({"name":item + r'.virtualDev',"type":"text"})

    return(dict,list)

def main():
    tmp_filepath = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/vmx/testVM.vmx'

    dict = {}
    dict["VM name"] = Vmx_displayName(tmp_filepath)
    dict["HW version"] = Vmx_virtualHWversion(tmp_filepath)
    dict["vCPU"] = Vmx_vCPU(tmp_filepath)
    dict["vMem"] = Vmx_vMem(tmp_filepath)

    dict1,list1 = Vmx_vDisk(tmp_filepath)
    dict2,list2 = Vmx_vNIC(tmp_filepath)
    dict3,list3 = Vmx_vBus(tmp_filepath)

    dict.update(dict1)
    dict.update(dict2)
    dict.update(dict3)
    dict_data = {"data":[dict]}

    list = []
    list.extend(list1)
    list.extend(list2)
    list.extend(list3)
    list.append({"name":"VM name"    ,"type":"text" })
    list.append({"name":"HW version" ,"type":"value"})
    list.append({"name":"vCPU"       ,"type":"value"})
    list.append({"name":"vMem"       ,"type":"text" })

    dict = {}
    dict = {
        "format": {
            "title": "VM Information",
            "labels":list,
        "hasHeader": True,
        "hasIndex": True
        }
    }

    dict.update(dict_data)

    json_file = open('../json/VM.json', 'w')
    json.dump(dict, json_file,indent=4)
    print(json.dumps(dict, json_file,indent=4))

main()
