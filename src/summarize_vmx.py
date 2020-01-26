import re

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

def Vmx_virtualHWversion(filepath):
    keyword = r'virtualHW.version = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vCPU(filepath):
    keyword = r'numvcpus = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vMem(filepath):
    keyword = r'memSize = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_ethernet(filepath):
    keyword = r'ethernet([0-9]).present = "TRUE"'
    list = SearchInVmx_AllDeviceNumber(filepath,keyword)

    for item in list:
        tmp = r'ethernet' + item + r'.virtualDev = "([a-zA-Z0-9]*)"'
        print('eth' + item + ' : ' + SearchInVmxText(filepath,tmp))
    
"""
def Vmx_scsi(filepath):
    keyword = r'scsi0:0.present = "(TRUE)"'
    return SearchInVmxText(filepath,keyword)
"""

def main():
    tmp_filepath = '/Volumes/Macintosh HDD/code/sano/testVM.vmx'

    a = Vmx_virtualHWversion(tmp_filepath)
    b = Vmx_vCPU(tmp_filepath)
    c = Vmx_vMem(tmp_filepath)
    Vmx_ethernet(tmp_filepath)
#    e = Vmx_scsi(tmp_filepath)

    print("HW version : " + a)
    print("vCPU : " + b)
    print("vMem : " + c)
 #   print("scsi : " + e)

main()
