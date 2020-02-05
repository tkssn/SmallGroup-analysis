import tarfile
import os
import datetime

def compress(path):
    tmp_targetdir = 'testfolder'
    now = datetime.datetime.now()
    os.chdir(path)

    with tarfile.open('AutoCompress_{0:%Y%m%d}'.format(now) + '_{0:%H%M%S}'.format(now) + '.tar.gz',mode='w:gz') as tf:
        tf.add(tmp_targetdir)

def main():
    tmp_path = '/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle'
    compress(tmp_path)

main()
