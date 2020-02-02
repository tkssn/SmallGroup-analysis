#!/bin/bash

target_dir="/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle/testfolder"
save_dir="/Volumes/Macintosh HDD/code/SmallGroup-analysis/LogBundle"
date=`date "+%Y%m%d_%H%M%S"`
save_file="/AutoCompress_$date.tar.gz"

tar  -czf "$save_dir$save_file" -C "$(dirname "$target_dir")" "$(basename "$target_dir")"
