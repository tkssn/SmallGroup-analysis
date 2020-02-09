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
    keyword = r'(.*build.*)'
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
    dict = {
        "format": {
            "title": "ESXi Information",
            "labels":[
                {"name":"HostVersion"   ,"type":"text"   },
                {"name":"ServerVendor"  ,"type":"text"   },
                {"name":"ServerModel"   ,"type":"text"   },
                {"name":"CPU Socket"    ,"type":"value"  },
                {"name":"CPU core"      ,"type":"value"  },
                {"name":"CPU Family"    ,"type":"value"  },
                {"name":"CPU model"     ,"type":"value"  },
                {"name":"Hyperthreading","type":"boolean"},
                {"name":"Memory Size"   ,"type":"text"  }
            ],
            "hasHeader": True,
            "hasIndex": True
        },
        "data":[
            {
            "HostVersion"  :HostVersion(tmp_currentpath),
            "ServerVendor" :ServerVendor(tmp_currentpath),
            "ServerModel"  :ServerModel(tmp_currentpath),
            "CPU Socket"   :CPUSocket(tmp_currentpath),
            "CPU core"     :CPUcore(tmp_currentpath),
            "CPU Family"   :CPUFamily(tmp_currentpath),
            "CPU model"    :CPUmodel(tmp_currentpath),
            "Hyperthrading":CPUHyperthreading(tmp_currentpath),
            "Memory size"  :MemoryInfo(tmp_currentpath)
            }
        ]
    }

    with open('../json/Hardware.json', 'w') as json_file:
        json.dump(dict, json_file,indent=4)
#    print(json.dumps(dict, json_file,indent=4))

main()
