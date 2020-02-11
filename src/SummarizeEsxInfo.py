import json
import re
import sys
import argparse

def SummarizeDisk(vmsupport_path):
    path = vmsupport_path + "/json/localcli_storage-core-device-list.json"
#   path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder/json/localcli_storage-core-device-list.json'

    with open(path) as f:
        df = json.load(f)
    list = []

    for i,j in enumerate(df):
        if df[i][u'Device Type'] == u'Direct-Access ':
            list.append({
                'ID'          :df[i][u'Device'],
                'Display Name':df[i][u'Display Name'],
                'Is Offline'  :df[i][u'Is Offline'],
                'Size'        :df[i][u'Size']
            })
    dict_data = {'date':list}

    dict = {
        "format": {
            "title": "Disk Information",
            "labels":[
                {"name":"ID"           ,"type":"text"   },
                {"name":"Display Name" ,"type":"value"  },
                {"name":"Is Offline"   ,"type":"boolean"},
                {"name":"Size"         ,"type":"value"}
            ],
            "hasHeader": True,
            "hasIndex": True
        }
    }

    dict.update(dict_data)

    with open('../json/Disk.json', 'w') as json_file:
        json.dump(dict,json_file,indent=4)
#       print(json.dumps(dict,indent=4))

def SummarizeDatastore(vmsupport_path):
    path = vmsupport_path + "/json/localcli_storage-filesystem-list--i.json"
#   path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder/json/localcli_storage-filesystem-list--i.json'

    with open(path) as f:
        df = json.load(f)

    list = []

    for i,j in enumerate(df):
        if df[i][u'Type'] == u'VMFS-5':
            list.append({
                'VMFS'          :df[i][u'Type'],
                'Size'          :df[i][u'Size'],
                'Free'          :df[i][u'Free'],
                'UUID'          :df[i][u'UUID'],
                'Mounted'       :df[i][u'Mounted'],
                'Datastore Name':df[i][u'Volume Name']
            })
    dict_data = {'date':list}

    dict = {
        "format": {
            "title": "Datastore Information",
            "labels":[
                {"name":"VMFS"           ,"type":"text"   },
                {"name":"Size"           ,"type":"value"  },
                {"name":"Free"           ,"type":"value"  },
                {"name":"UUID"           ,"type":"text"   },
                {"name":"Mounted"        ,"type":"boolean"},
                {"name":"Datastore Name" ,"type":"text"   }
            ],
            "hasHeader": True,
            "hasIndex": True
        }
    }

    dict.update(dict_data)

    with open('../json/Datastore.json', 'w') as json_file:
        json.dump(dict,json_file,indent=4)
#       print(json.dumps(dict,indent=4))

def SummarizeHardware(path):
#   path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder'

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
            "HostVersion"  :HostVersion(path),
            "ServerVendor" :ServerVendor(path),
            "ServerModel"  :ServerModel(path),
            "CPU Socket"   :CPUSocket(path),
            "CPU core"     :CPUcore(path),
            "CPU Family"   :CPUFamily(path),
            "CPU model"    :CPUmodel(path),
            "Hyperthrading":CPUHyperthreading(path),
            "Memory size"  :MemoryInfo(path)
            }
        ]
    }

    with open('../json/Hardware.json', 'w') as json_file:
        json.dump(dict, json_file,indent=4)
#       print(json.dumps(dict, json_file,indent=4))

def SummarizeVirtualNetwork(vmsupport_path):
    path = vmsupport_path + "/commands/esxcfg-info_-a.txt"
#   path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder/commands/esxcfg-info_-a.txt'

    with open(path) as f:
        lines = f.readlines()
    lines_strip = [line.strip() for line in lines] ####

    for a,line in enumerate(lines_strip):
        if '\==+Network Entities :' in line:
            NW_Entities = a

    list = []

    for i,line in enumerate(lines_strip):
        if '\==+Virtual Switch :' in line:
            if i > NW_Entities:
                # vSwitch Name
                keyword = r'\|----Name\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+1])
                vSwitch_Name = matchword.group(1)

                # vSwitch Uplinks
                keyword = r'\|----Uplinks\.*(.*)' 
                matchword = re.match(keyword,lines_strip[i+2])
                vSwitch_Uplinks = matchword.group(1)

                # vSwitch MTU
                keyword = r'\|----MTU\.*(.*)' 
                matchword = re.match(keyword,lines_strip[i+11])
                vSwitch_MTU = matchword.group(1)

                list.append({
                    'vSwitch Name'    :vSwitch_Name,
                    'vSwitch Uplinks' :vSwitch_Uplinks,
                    'vSwitch MTU'     :vSwitch_MTU
                })

        if '\==+VmKernel Nic :' in line:
            if i > NW_Entities:
                # VMkernel Port Group
                keyword = r'\|----Port Group\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+1])
                VMkernel_PortGroup = matchword.group(1)

                # VMkernel Interface
                keyword = r'\|----Interface\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+3])
                VMkernel_Interface = matchword.group(1)

                # VMKernel MTU
                keyword = r'\|----MTU\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+6])
                VMkernel_MTU = matchword.group(1)

                # VMkernel Tags
                keyword = r'\|----Tags\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+9])
                VMkernel_Tags = matchword.group(1)

                # VMkernel IPv4 Address
                keyword = r'\|----IPv4 Address\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+13])
                VMkernel_IPv4Address = matchword.group(1)

                # VMkernel IPv4 Netmask
                keyword = r'\|----IPv4 Netmask\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+14])
                VMkernel_IPv4Netmask = matchword.group(1)

                list.append({
                    'VMkernel Port Group'   :VMkernel_PortGroup,
                    'VMkernel Interface'    :VMkernel_Interface,
                    'VMkernel MTU'          :VMkernel_MTU,
                    'VMkernel Tags'         :VMkernel_Tags,
                    'VMkernel IPv4 Address' :VMkernel_IPv4Address,
                    'VMkernel IPv4 Netmask' :VMkernel_IPv4Netmask
                })
                
        if '\==+Port Groups :' in line:
            if i > NW_Entities:
                # Portgroup Name
                keyword = r'\|----Name\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+2])
                PortGroup_Name = matchword.group(1)

                # Mapping between Portgroup and vSwitch
                keyword = r'\|----Virtual Switch\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+3])
                PortGroup_vSwitch = matchword.group(1)

                # Portgroup VLAN
                keyword = r'\|----Vlan Id\.*(.*)'
                matchword = re.match(keyword,lines_strip[i+5])
                PortGroup_VLAN = matchword.group(1)

                list.append({
                    'Portgroup Name'    :PortGroup_Name,
                    'Portgroup vSwitch' :PortGroup_vSwitch,
                    'Portgroup VLAN'    :PortGroup_VLAN
                })
                
    dict_data = {'data' :list}

    dict = {
        "format": {
            "title": "Virtual Network Information",
            "labels":[
                {"name":"vSwitch Name"          ,"type":"text" },
                {"name":"vSwitch Uplinks"       ,"type":"text" },
                {"name":"vSwitch MTU"           ,"type":"value"},
                {"name":"VMkernel Port Group"   ,"type":"text" },
                {"name":"VMkernel Interface"    ,"type":"text" },
                {"name":"VMkernel MTU"          ,"type":"value"},
                {"name":"VMkernel Tags"         ,"type":"text" },
                {"name":"VMkernel IPv4 Address" ,"type":"text" },
                {"name":"VMkernel IPv4 Netmask" ,"type":"text" },
                {"name":"Portgroup Name"        ,"type":"text" },
                {"name":"Portgroup vSwitch"     ,"type":"text" },
                {"name":"Portgroup VLAN"        ,"type":"value"}
            ],
            "hasHeader": True,
            "hasIndex": True
        }
    }

    dict.update(dict_data)

    with open('../json/vNetwork.json', 'w') as json_file:
        json.dump(dict,json_file,indent=4)
#       print(json.dumps(dict,indent=4))

def main():
    parser = argparse.ArgumentParser(prog='SummarizeEsxInfo.py',usage='Summarize ESXi Information',description='description',epilog='end',add_help=True)
    parser.add_argument('-f', '--file',help='input the vm-support directory',type=str,required=True)
    args = parser.parse_args()
    vmsupport_path =  args.file

    SummarizeDisk(vmsupport_path)
    SummarizeDatastore(vmsupport_path)
    SummarizeHardware(vmsupport_path)
    SummarizeVirtualNetwork(vmsupport_path)

main()

