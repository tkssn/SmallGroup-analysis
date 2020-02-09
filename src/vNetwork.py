import sys
import re
import json

path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder/commands/esxcfg-info_-a.txt'

with open(path) as f:
    lines = f.readlines()
lines_strip = [line.strip() for line in lines]

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
# print(json.dumps(dict,indent=4))

