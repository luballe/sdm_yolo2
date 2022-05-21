#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
pwd_cmd='pwd'
current_path=$(eval "$pwd_cmd")'/'
#folder="/monitoreo/Aforos_CGT/2020_06_10/2_AK 72 X AC 53/1700_1900/test"
folder="$1"
pickle="$2"
#folder="$folder""/results"
folder="$folder"
cd /home/administrador/sdm_yolo/python
python2 aforo_unattended_2.py "$folder" "$pickle"
cd $current_path
