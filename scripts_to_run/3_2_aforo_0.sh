#!/bin/bash
# Usage: 3_aforo_0.sh "/path/to_results/" "/path/to_pickle"
export CUDA_VISIBLE_DEVICES=0
pwd_cmd='pwd'
current_path=$(eval "$pwd_cmd")'/'
#folder="/monitoreo/Aforos_CGT/2020_06_10/2_AK 72 X AC 53/1700_1900/results"
file="$1"
pickle="$2"
#folder="$folder""/results"
#file="$file"
cd /monitoreo/sdm_yolo/sdm_yolo/python
python2 aforo_unattended_single_file_1.py "$file" "$pickle"
cd $current_path
