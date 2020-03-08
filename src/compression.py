import tarfile
import os
import datetime
import argparse

SourceFileDirname = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()

def errorLog(e):
    os.chdir(SourceFileDirname)
    with open('compression.log','ab') as fp:
        fp.write('{0:%Y-%m-%d %H:%M:%S}'.format(now) + ' ErrorMsg: ' + str(e) + '\n')

def compress(path):
    targetDirname = os.path.basename(path)
    os.chdir(os.path.dirname(path))

    try:
        with tarfile.open(targetDirname + '_{0:%y%m%d}'.format(now) + '_{0:%H%M%S}'.format(now) + '.tar.gz',mode='w:gz') as tf:
            tf.add(targetDirname)
    except Exception as e:
        errorLog(e)

def main():
    
    parser = argparse.ArgumentParser(prog='compression.py',usage='Compress files',description='description',epilog='end',add_help=True)
    parser.add_argument('-f', '--file',help='input the target directory',type=str,required=True)
    args = parser.parse_args()
    targetPath =  args.file

    compress(targetPath)

main()
