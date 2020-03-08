import os
import tarfile
import re
import gzip
import shutil
import datetime
import argparse

SourceFileDirname = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()

def errorLog(e):
    os.chdir(SourceFileDirname)
    with open('extractEsxLogBundle.log','ab') as fp:
        fp.write('{0:%Y-%m-%d %H:%M:%S}'.format(now) + ' ErrorMsg: ' + str(e) + '\n')

def ExtractVmSupportLog(filepath):
    extractDirpath = os.path.join(os.path.dirname(filepath), 'extract_' + '{0:%y%m%d_%H%M%S}'.format(now))
    
    try:
        with tarfile.open(filepath, 'r') as tf:
            tf.extractall(path=extractDirpath)
    except Exception as e:
        errorLog(e)

    for curDir, dirs, files in os.walk(extractDirpath):
        for filename in files:
            if filename.endswith(".gz"):
                InputFile = os.path.join(curDir,filename)
                OutputFile = os.path.join(curDir,os.path.splitext(filename)[0])
                try:
                    with gzip.open(InputFile,'rb') as f_in:
                        with open(OutputFile, 'wb') as f_out:
                            shutil.copyfileobj(f_in,f_out)
                    os.remove(InputFile)
                except Exception as e:
                    errorLog(e)

    extractVmsupportName = os.listdir(extractDirpath)[0]

    return extractDirpath,extractVmsupportName

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
        try:
            with open(os.path.join(dirpath, orgfile), 'wb') as fporg:
                for fragment in targets[orgfile]:
                    filepath = os.path.join(dirpath, fragment)
                    with open(filepath, 'rb') as fpfrag:
                        fporg.write(fpfrag.read())
                    os.remove(filepath)
        except Exception as e:
            errorLog(e)
    return True

def CleanFile(filepath, delword):
    if not os.path.exists(filepath):
        return False
    #
    logfile = filepath
    tmpfile = filepath + '.tmp'
    repattern = re.compile(delword)
    try:
        os.rename(filepath, tmpfile)
        with open(filepath, 'w') as fpwrite:
            with open(tmpfile, 'r') as fpread:
                for line in fpread:
                    match = repattern.match(line)
                    if not match:
                        fpwrite.write(line)
        os.remove(tmpfile)
    except Exception as e:
        if os.path.exists(tmpfile):
            if os.path.exists(logfile):
                os.remove(logfile)
            os.rename(tmpfile, filepath)
        errorLog(e)
        return False
    return True

def MergeLogFiles(dirpath):
    MergeLogTypePaths = []
    for curDir, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".0"):
                MergeLogTypePaths.append(os.path.splitext(os.path.join(curDir, file))[0])
    # vmsyslogd-dropped.log
    for curDir, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith(".1"):
                if not os.path.splitext(os.path.join(curDir, file))[0] in MergeLogTypePaths:
                    MergeLogTypePaths.append(os.path.splitext(os.path.join(curDir, file))[0])

    MergeLogContents = []
    for MergeLogTypePath in MergeLogTypePaths:
        for curDir, dirs, files in os.walk(os.path.dirname(MergeLogTypePath)):
            for file in files:
                if file.startswith(os.path.basename(MergeLogTypePath) + '.'):
                    MergeLogContents.append(file)

        MergeLogContents = sorted(MergeLogContents,reverse=True)
        for MergeLogContent in MergeLogContents:
            if os.path.splitext(MergeLogContent)[1] == '.log':
                MergeLogContents.remove(MergeLogContent)
                MergeLogContents.append(MergeLogContent)

        try:
            with open(MergeLogTypePath + '_all.log','ab') as saveFile:
                for MergeLogContent in MergeLogContents:
                    with open(os.path.join(os.path.dirname(MergeLogTypePath),MergeLogContent),'rb') as fp:
                        saveFile.write(fp.read())
                    os.remove(os.path.join(os.path.dirname(MergeLogTypePath),MergeLogContent))
            os.rename(MergeLogTypePath + '_all.log', MergeLogTypePath + '.log')
        except Exception as e:
            errorLog(e)

        MergeLogContents = []

def MergeVmwarelogFiles(dirpath):
    MergeVmwarelogPaths = []
    for curDir, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith("vmware.log"):
                MergeVmwarelogPaths.append(os.path.dirname((os.path.join(curDir, file))))

    MergeVmwarelogContents = []
    for MergeVmwarelogPath in MergeVmwarelogPaths:
        for curDir, dirs, files in os.walk(MergeVmwarelogPath):
            for file in files:
                if file.startswith("vmware") and file.endswith(".log"):
                    MergeVmwarelogContents.append(file)
        MergeVmwarelogContents = sorted(MergeVmwarelogContents, reverse=False)

        try:
            with open(os.path.join(MergeVmwarelogPath,'vmware_all.log'),'ab') as saveFile:
                for MergeVmwarelogContent in MergeVmwarelogContents:
                    with open(os.path.join(MergeVmwarelogPath,MergeVmwarelogContent),'rb') as fp:
                        saveFile.write(fp.read())
                    os.remove(os.path.join(MergeVmwarelogPath,MergeVmwarelogContent))
            os.rename(os.path.join(MergeVmwarelogPath,'vmware_all.log'),os.path.join(MergeVmwarelogPath,'vmware.log'))
        except Exception as e:
            errorLog(e)

        MergeVmwarelogContents = []

def ChangeFileMode(dirpath):
    try:
        for curDir, dirs, files in os.walk(dirpath):
            for file in files:
                os.chmod(os.path.join(curDir,file),0444)
    except Exception as e:
        errorLog(e)

def main():
    parser = argparse.ArgumentParser(prog='extractLogBundle.py',usage='Extract the log bundle',description='description',epilog='end',add_help=True)
    parser.add_argument('-f', '--file',help='input the target directory',type=str,required=True)
    args = parser.parse_args()
    targetLogBundlePath =  args.file

    extractContents = ExtractVmSupportLog(targetLogBundlePath)

    targetMergeFileFragmentsDir = os.path.join(extractContents[0],extractContents[1],'commands')
    MergeFileFragments(targetMergeFileFragmentsDir)
    targetCleanFileDir = os.path.join(extractContents[0],extractContents[1],'commands','esxcfg-info_-a--F-xml.txt')
    CleanFile(targetCleanFileDir, r"^ResourceGroup:.*")

    targetMergeLogDir = os.path.join(extractContents[0],extractContents[1],'var')
    MergeLogFiles(targetMergeLogDir)

    MergeVmwarelogFiles(os.path.join(extractContents[0],extractContents[1],'vmfs','volumes'))

    ChangeFileMode(extractContents[0])

main()
