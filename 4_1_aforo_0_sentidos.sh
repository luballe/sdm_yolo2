#!/bin/bash
# Usage: 3_aforo_0.sh "/path/to_results/" "/path/to_pickle"
START_TIME=$SECONDS
export CUDA_VISIBLE_DEVICES=0
pwd_cmd='pwd'
current_path=$(eval "$pwd_cmd")'/'
#folder="/monitoreo/Aforos_CGT/2020_06_10/2_AK 72 X AC 53/1700_1900/results"
IFS=' ' read -ra args <<< "$1"
file="${args[0]}"
pickle="${args[1]}"
num_files=$2
current_process=$3
echo "*** Started "$current_process"/"$num_files" ***"
echo "File: "$file 
echo "Pickle: "$pickle
#folder="$folder""/results"
#file="$file"
cd /monitoreo/sdm_yolo/sdm_yolo/python
python2 aforo_unattended_sentidos.py "$file" "$pickle"
sleep 20
cd $current_path
ELAPSED_TIME=$(($SECONDS - $START_TIME))
echo "Done "$current_process"/"$num_files " in "$ELAPSED_TIME" seconds - "$(date)
