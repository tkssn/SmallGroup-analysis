import os
import tarfile
import os
import gzip
import shutil

def ExtractVmSupportLog(filepath):
    tmp_path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle'   
    t = tarfile.open(filepath, 'r')
    t.extractall(tmp_path)

    for curDir, dirs, files in os.walk(tmp_path):
        for filename in files:
            if filename.endswith(".gz"):
                tmp1 = os.path.join(curDir,filename)
                tmp2 = os.path.join(curDir,os.path.splitext(filename)[0])
                with gzip.open(tmp1,'rb') as f_in:
                    with open(tmp2, 'wb') as f_out:
                        shutil.copyfileobj(f_in,f_out)
                os.remove(tmp1)

def main():
    tmp_filepath = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/172.16.0.13-vmsupport-2020-01-08@11-47-04.tgz'
    ExtractVmSupportLog(tmp_filepath)

main()
