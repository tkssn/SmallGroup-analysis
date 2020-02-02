import re
import json

def SearchInEsxInfo(filepath,keyword):
    with open(filepath,'r') as fp:
        for line in fp:
            matchword = re.match(keyword,line)
            if matchword:
                return matchword.group(1)

def HostVersion(filepath):
    targetpath = filepath + '/commands/vmware_-vl.txt'
    keyword = r'VMware ESXi (6.0.0 build-10719132)'
    return SearchInEsxInfo(targetpath,keyword)

def ServerVendor(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Vendor Name\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)    

def ServerModel(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Product Name\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def CPUSocket(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Num Packages\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def CPUcore(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Num Cores\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def CPUFamily(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Family\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def CPUmodel(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Model\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def CPUHyperthreading(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Hyperthreading Active\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def MemoryInfo(filepath):
    targetpath = filepath + '/commands/esxcfg-info_-a.txt'
    keyword = r'.*Physical Mem\.*(.*)'
    return SearchInEsxInfo(targetpath,keyword)

def main():
    tmp_currentpath = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder'
    dict = {}

    dict['HostVersion']   = HostVersion(tmp_currentpath)
    dict['ServerVendor']  = ServerVendor(tmp_currentpath)
    dict['ServerModel']   = ServerModel(tmp_currentpath)
    dict['CPU Socket']    = CPUSocket(tmp_currentpath)
    dict['CPU core']      = CPUcore(tmp_currentpath)
    dict['CPU Family']    = CPUFamily(tmp_currentpath)
    dict['CPU model']     = CPUmodel(tmp_currentpath)
    dict['Hyperthrading'] = CPUHyperthreading(tmp_currentpath)
    dict['memory size']   = MemoryInfo(tmp_currentpath)

    json_file = open('../json/test.json', 'w')
    json.dump(dict, json_file)

main()
