import os
import re

def MergeFileFragments(dirpath, suffix=r"[.]FRAG-[0-9]{5}", debug=False):
    if not os.path.exists(dirpath):
        return False
    #
    repattern = re.compile(r"^(.*)%s$" % suffix)
    targets = {}
    for filename in os.listdir(dirpath):
        match = repattern.match(filename)
        if match:
            orgfile = match.groups()[0]
            if not orgfile in targets:
                targets[orgfile] = []
            targets[orgfile].append(filename)
    #
    for orgfile in targets.keys():
        targets[orgfile].sort()
        with open(os.path.join(dirpath, orgfile), 'wb') as fporg:
            for fragment in targets[orgfile]:
                filepath = os.path.join(dirpath, fragment)
                with open(filepath, 'rb') as fpfrag:
                    fporg.write(fpfrag.read())
                os.remove(filepath)
    return True


def main():
    tmp_path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder/commands'

    MergeFileFragments(tmp_path)


main()
