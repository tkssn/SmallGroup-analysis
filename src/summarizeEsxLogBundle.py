import json
import re
import sys
import os
import xml.etree.ElementTree as et
import argparse
import datetime

SourceFileDirname = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()

def errorLog(e):
    os.chdir(SourceFileDirname)
    with open('summarizeEsxLogBundle.log','ab') as fp:
        fp.write('{0:%Y-%m-%d %H:%M:%S}'.format(now) + ' ErrorMsg: ' + str(e) + '\n')

def SearchKeyword(filepath,keyword):
    with open(filepath,'r') as fp:
        for line in fp:
            matchword = re.match(keyword,line)
            if matchword:
                return matchword.group(1)

def SearchInXML(xpath,root):
    elements = root.findall(xpath)
    for element in elements:
        return element.text

def SearchMultiInXML(xpath,root):
    elements = root.findall(xpath)
    return elements

def SummarizeDisk(path):
    path = os.path.join(path,'json','localcli_storage-core-device-list.json')

    try:
        with open(path) as fp:
            df = json.load(fp)
    except Exception as e:
        errorLog(e)

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

    try:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','Disk.json'), 'w') as json_file:
            json.dump(dict,json_file,indent=4)
    except Exception as e:
        errorLog(e)

def SummarizeDatastore(path):
    path = os.path.join(path,'json','localcli_storage-filesystem-list--i.json')

    try:
        with open(path) as fp:
            df = json.load(fp)
    except Exception as e:
        errorLog(e)

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

    try:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','Datastore.json'), 'w') as json_file:
            json.dump(dict,json_file,indent=4)
    except Exception as e:
        errorLog(e)

def SummarizeHardware(path):
    XMLpath = os.path.join(path,"commands","esxcfg-info_-a--F-xml.txt")
    tree = et.parse(XMLpath)
    root = tree.getroot()

    def ServerVendor(filepath,root):
        xpath = r'./hardware-info/value[@name="vendor-name"]'
        return SearchInXML(xpath,root)

    def ServerModel(filepath,root):
        xpath = r'./hardware-info/value[@name="product-name"]'
        return SearchInXML(xpath,root)

    def CPUSocket(filepath,root):
        xpath = r'./hardware-info/cpu-info/value[@name="num-packages"]'
        return SearchInXML(xpath,root)

    def CPUcore(filepath,root):
        xpath = r'./hardware-info/cpu-info/value[@name="num-cores"]'
        return SearchInXML(xpath,root)

    def CPUHyperthreading(filepath,root):
        xpath = r'./hardware-info/cpu-info/value[@name="hyperthreading-active"]'
        return SearchInXML(xpath,root)

    def MemoryInfo(filepath,root):
        xpath = r'./hardware-info/memory-info/value[@name="physical-mem"]'
        return SearchInXML(xpath,root)

    dict = {
        "format": {
            "title": "Hardware Information",
            "labels":[
                {"name":"Content" ,"type":"text"},
                {"name":"Detail"  ,"type":"text"}
            ],
            "hasHeader": True,
            "hasIndex": True
        },
        "data":[
            {
                "Content":"Server Vendor",
                "Detail" :ServerVendor(XMLpath,root)
            },
            {
                "Content":"Server Model",
                "Detail" :ServerModel(XMLpath,root)
            },
            {
                "Content":"CPU Socket",
                "Detail" :CPUSocket(XMLpath,root)
            },
            {
                "Content":"CPU Core",
                "Detail" :CPUcore(XMLpath,root)
            },
            {
                "Content":"Hyperthreading Enabled",
                "Detail" :CPUHyperthreading(XMLpath,root)
            },
            {
                "Content":"Memory Size",
                "Detail" :MemoryInfo(XMLpath,root)
            }
        ]
    }

    try:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','Hardware.json'), 'w') as json_file:
            json.dump(dict, json_file,indent=4)
    except Exception as e:
        errorLog(e)

def SummarizeStorageAdapter(path):
    XMLpath = os.path.join(path,"commands","esxcfg-info_-a--F-xml.txt")
    tree = et.parse(XMLpath)
    root = tree.getroot()
    
    xpath = r'./storage-info/all-scsi-iface/*/scsi-interface/value[@name="name"]'
    StorageAdapterNames = SearchMultiInXML(xpath,root)

    xpath = r'./storage-info/all-scsi-iface/*/scsi-interface/value[@name="driver"]'
    StorageAdapterDrivers = SearchMultiInXML(xpath,root)

    xpath = r'./storage-info/all-scsi-iface/*/scsi-interface/pci-device/value[@name="vendor-name"]'
    StorageAdapterVendors = SearchMultiInXML(xpath,root)

    xpath = r'./storage-info/all-scsi-iface/*/scsi-interface/pci-device/value[@name="device-name"]'
    StorageAdapterDevices = SearchMultiInXML(xpath,root)

    list = []
    for StorageAdapterName, StorageAdapterDriver, StorageAdapterVendor, StorageAdapterDevice in zip(StorageAdapterNames, StorageAdapterDrivers, StorageAdapterVendors, StorageAdapterDevices):
        list.append({
            "HBA Name"   :StorageAdapterName.text,
            "driver"     :StorageAdapterDriver.text,
            "Vendor"     :StorageAdapterVendor.text,
            "Device"     :StorageAdapterDevice.text
        })
        
    dict = {
        "format": {
            "title": "Storage Adapter Information",
            "labels":[
                {"name":"HBA Name"  ,"type":"text"},
                {"name":"driver"    ,"type":"text"},
                {"name":"Vendor"    ,"type":"text"},
                {"name":"Device"    ,"type":"text"}
            ],
            "hasHeader": True,
            "hasIndex": True
        },
        "data":list
    }

    try:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','StorageAdapter.json'), 'w') as json_file:
            json.dump(dict,json_file,indent=4)
    except Exception as e:
        errorLog(e)

def SummarizeVirtualNetwork(path):
    def SummarizeVirtualSwitch(path,root):
        xpath = r'./network-info/virtual-switch-info/virtual-switches/virtual-switch/value[@name="name"]'
        vSwitchNames = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/virtual-switch-info/virtual-switches/virtual-switch/value[@name="uplinks"]'
        vSwitchUplinks = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/virtual-switch-info/virtual-switches/virtual-switch/value[@name="mtu"]'
        vSwitchMTUs = SearchMultiInXML(xpath,root)

        list = []
        for vSwitchName, vSwitchUplink, vSwitchMTU in zip(vSwitchNames, vSwitchUplinks, vSwitchMTUs):
            list.append({
                "Display Name":vSwitchName.text,
                "Uplink":vSwitchUplink.text,
                "MTU":vSwitchMTU.text
                })
        
        dict = {
            "format": {
                "title": "vSwitch Information",
                "labels":[
                    {"name":"Display Name" ,"type":"text" },
                    {"name":"Uplink"       ,"type":"text" },
                    {"name":"MTU"          ,"type":"value"}
                ],
                "hasHeader": True,
                "hasIndex": True
            },
            "data":list
        }

        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','vSwitch.json'), 'w') as json_file:
                json.dump(dict,json_file,indent=4)
        except Exception as e:
            errorLog(e)

    def SummarizePortgroup(path,root):
        xpath = r'./network-info/virtual-switch-info/virtual-switches/virtual-switch/port-groups/port-group/value[@name="name"]'
        PortgroupNames = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/virtual-switch-info/virtual-switches/virtual-switch/port-groups/port-group/value[@name="virtual-switch"]'
        PortgroupVswitches = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/virtual-switch-info/virtual-switches/virtual-switch/port-groups/port-group/value[@name="vlan-id"]'
        PortgroupVlans = SearchMultiInXML(xpath,root)

        list = []
        for PortgroupName, PortgroupVswitch, PortgroupVlan in zip(PortgroupNames, PortgroupVswitches, PortgroupVlans):
            list.append({
                "Port Group Name":PortgroupName.text,
                "vSwitch"        :PortgroupVswitch.text,
                "VLAN"           :PortgroupVlan.text
            })

        dict = {
            "format": {
                "title": "Port Group Information",
                "labels":[
                    {"name":"Port Group Name", "type":"text" },
                    {"name":"vSwitch"        , "type":"text" },
                    {"name":"VLAN"           , "type":"value"}
                ],
                "hasHeader": True,
                "hasIndex": True
            },
            "data":list
        }

        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','Portgroup.json'), 'w') as json_file:
                json.dump(dict,json_file,indent=4)
        except Exception as e:
            errorLog(e)

    def SummarizeVMkernel(path,root):#<--- Need to test multiple vmkernel
        xpath = r'./network-info/vmkernel-nic-info/kernel-nics/vmkernel-nic/value[@name="port-group"]'
        vmkernelPortgroups = SearchMultiInXML(xpath,root) 

        xpath = r'./network-info/vmkernel-nic-info/kernel-nics/vmkernel-nic/value[@name="interface"]'
        vmkernelInterfaces = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/vmkernel-nic-info/kernel-nics/vmkernel-nic/value[@name="mtu"]'
        vmkernelMtus = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/vmkernel-nic-info/kernel-nics/vmkernel-nic/value[@name="tags"]'
        vmkernelTags = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/vmkernel-nic-info/kernel-nics/vmkernel-nic/actual-ip-settings/ipv4-settings/value[@name="ipv4-address"]'
        vmkernelIpv4addresses = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/vmkernel-nic-info/kernel-nics/vmkernel-nic/actual-ip-settings/ipv4-settings/value[@name="ipv4-netmask"]'
        vmkernelIpv4netmasks = SearchMultiInXML(xpath,root)

        list = []
        for vmkernelPortgroup,vmkernelInterface,vmkernelMtu,vmkernelTag,vmkernelIpv4address,vmkernelIpv4netmask in zip(vmkernelPortgroups,vmkernelInterfaces,vmkernelMtus,vmkernelTags,vmkernelIpv4addresses,vmkernelIpv4netmasks):
            list.append({
                "Port Group"  :vmkernelPortgroup.text,
                "Interface"   :vmkernelInterface.text,
                "MTU"         :vmkernelMtu.text,
                "Type"        :vmkernelTag.text,
                "IPv4 Address":vmkernelIpv4address.text,
                "IPv4 Netmask":vmkernelIpv4netmask.text
            })

        dict = {
            "format": {
                "title": "VMkernel Information",
                "labels":[
                    {"name":"Port Group"  , "type":"text" },
                    {"name":"Interface"   , "type":"text" },
                    {"name":"MTU"         , "type":"value"},
                    {"name":"Type"        , "type":"text"},
                    {"name":"IPv4 Address", "type":"text"},
                    {"name":"IPv4 Netmask", "type":"text"}
                ],
                "hasHeader": True,
                "hasIndex": True
            },
            "data":list
        }

        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','VMkernel.json'), 'w') as json_file:
                json.dump(dict,json_file,indent=4)
        except Exception as e:
            errorLog(e)

    def SummarizePhysicalNIC(path,root):
        xpath = r'./network-info/physical-nics/physical-nic/value[@name="name"]'
        PhysicalNICNames = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/value[@name="mac-address"]'
        PhysicalNICMacAddresses = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/value[@name="driver"]'
        PhysicalNICDrivers = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/value[@name="mtu"]'
        PhysicalNICMTUs = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/value[@name="actual-speed"]'
        PhysicalNICSpeeds = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/value[@name="link-up"]'
        PhysicalNICLinkUps = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/pci-device/value[@name="vendor-name"]'
        PhysicalNICVendors = SearchMultiInXML(xpath,root)

        xpath = r'./network-info/physical-nics/physical-nic/pci-device/value[@name="device-name"]'
        PhysicalNICDevices = SearchMultiInXML(xpath,root)

        list = []
        for PhysicalNICName, PhysicalNICMacAddress, PhysicalNICDriver, PhysicalNICMTU, PhysicalNICSpeed, PhysicalNICLinkUp, PhysicalNICVendor, PhysicalNICDevice in zip(PhysicalNICNames, PhysicalNICMacAddresses, PhysicalNICDrivers, PhysicalNICMTUs, PhysicalNICSpeeds, PhysicalNICLinkUps, PhysicalNICVendors, PhysicalNICDevices):
            list.append({
                "Name"           :PhysicalNICName.text,
                "Mac Address"    :PhysicalNICMacAddress.text,
                "Driver"         :PhysicalNICDriver.text,
                "MTU"            :PhysicalNICMTU.text,
                "Speed"          :PhysicalNICSpeed.text,
                "Link Up Status" :PhysicalNICLinkUp.text,
                "Vendor"         :PhysicalNICVendor.text,
                "Device"         :PhysicalNICDevice.text
            })

        dict = {
            "format": {
                "title": "Physical NIC Information",
                "labels":[
                    {"name":"Name"          , "type":"text"   },
                    {"name":"Mac Address"   , "type":"text"   },
                    {"name":"Driver"        , "type":"text"   },
                    {"name":"MTU"           , "type":"value"  },
                    {"name":"Speed"         , "type":"value"  },
                    {"name":"Link Up Status", "type":"boolean"},
                    {"name":"Vendor"        , "type":"text"   },
                    {"name":"Device"        , "type":"text"   }
                ],
                "hasHeader": True,
                "hasIndex": True
            },
            "data":list
        }

        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','PhysicalNIC.json'), 'w') as json_file:
                json.dump(dict,json_file,indent=4)
        except Exception as e:
            errorLog(e)


    XMLpath = os.path.join(path,"commands","esxcfg-info_-a--F-xml.txt")
    tree = et.parse(XMLpath)
    root = tree.getroot()

    SummarizeVirtualSwitch(XMLpath,root)
    SummarizeVMkernel(XMLpath,root)
    SummarizePortgroup(XMLpath,root)
    SummarizePhysicalNIC(XMLpath,root)

def SummarizeEsxInfo(path):
    XMLpath = os.path.join(path,"commands","esxcfg-info_-a--F-xml.txt")
    tree = et.parse(XMLpath)
    root = tree.getroot()

    def HostVersion(filepath):
        targetpath = os.path.join(filepath,'commands','vmware_-vl.txt')
        keyword = r'(.*build.*)'
        return SearchKeyword(targetpath,keyword)
    
    def PowerManagement(filepath,root):
        xpath = r'./hardware-info/cpu-power-management-info/value[@name="current-policy"]'
        return SearchInXML(xpath,root)

    dict = {
        "format": {
            "title": "ESXi Information",
            "labels":[
                {"name":"Content" ,"type":"text"},
                {"name":"Detail"  ,"type":"text"}
            ],
            "hasHeader": True,
            "hasIndex": True
        },
        "data":[
            {
                "Content":"ESXi Version",
                "Detail" :HostVersion(path)
            },
            {
                "Content":"PowerManagement",
                "Detail" :PowerManagement(path,root)
            }
        ]
    }

    try:
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'json','ESXiInformation.json'), 'w') as json_file:
            json.dump(dict, json_file,indent=4)
    except Exception as e:
        errorLog(e)

def main():
    vmsupport_path = "/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder"
    """
    parser = argparse.ArgumentParser(prog='SummarizeEsxInfo.py',usage='Summarize ESXi Information',description='description',epilog='end',add_help=True)
    parser.add_argument('-f', '--file',help='input the vm-support directory',type=str,required=True)
    args = parser.parse_args()
    vmsupport_path = args.file
    """

    if os.path.isdir(vmsupport_path) == True:
        SummarizeDisk(vmsupport_path)
        SummarizeDatastore(vmsupport_path)
        SummarizeHardware(vmsupport_path)
        SummarizeVirtualNetwork(vmsupport_path)
        SummarizeEsxInfo(vmsupport_path)
        SummarizeStorageAdapter(vmsupport_path)
    else:
        errorLog("vm-support doesn't exist")

main()
