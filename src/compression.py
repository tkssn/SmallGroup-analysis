import tarfile
import os
import datetime
import argparse

def compress(path):
    targetdir = os.path.basename(path)
    now = datetime.datetime.now()
    os.chdir(os.path.dirname(path))

    with tarfile.open(targetdir + '_{0:%y%m%d}'.format(now) + '_{0:%H%M%S}'.format(now) + '.tar.gz',mode='w:gz') as tf:
        tf.add(targetdir)

def main():
    parser = argparse.ArgumentParser(prog='compression.py',usage='Compress files',description='description',epilog='end',add_help=True)
    parser.add_argument('-f', '--file',help='input the target directory',type=str,required=True)
    args = parser.parse_args()

    target_path =  args.file
#   target_path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder'

    compress(target_path)


main()
