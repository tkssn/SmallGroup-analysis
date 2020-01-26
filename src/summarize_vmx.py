import re

def SearchInVmxText(filepath,keyword):
    with open(filepath,'r') as fp:
        for line in fp:
            matchword = re.match(keyword,line)
            if matchword:
                return matchword.group(1)

def Vmx_virtualHWversion(filepath):
    keyword = r'virtualHW.version = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def Vmx_vCPU(filepath):
    keyword = r'maxvcpus = "([0-9]*)"'
    return SearchInVmxText(filepath,keyword)

def main():
    tmp_filepath = '/Volumes/Macintosh HDD/code/sano/Windows for Workgroups 3.11.vmx'
    a = Vmx_virtualHWversion(tmp_filepath)
    b = Vmx_vCPU(tmp_filepath)

    print(a)
    print(b)

main()
