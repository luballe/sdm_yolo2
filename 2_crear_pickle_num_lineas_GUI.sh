#!/bin/bash
# Usage:
# ./2_crear_pickle_num_lienasGUI.sh /path/to_video_files <num_lineas>
# ./2_crear_pickle_num_lineasGUI.sh /monitoreo/videos/0600_0800/results <num_lineas>
pwd_cmd='pwd'
current_path=$(eval "$pwd_cmd")'/'
#folder="/monitoreo/Aforos_CGT/2020_06_12/1_AK 7 X AC 72/0600_0800"
folder="$1"
num_lineas="$2"
cd /monitoreo/sdm_yolo/sdm_yolo/python
python2 Crear_pickle_num_lineas.py "$folder" $num_lineas
#cd "$folder"
#mkdir "results"
#cp "config.pkl" "results"
#cd ..
#mkdir -p "1100_1400/results"
#cp "0600_0800/config.pkl" "1100_1400/results"
#mkdir -p "1700_1900/results"
#cp "0600_0800/config.pkl" "1700_1900/results"

#cd $current_path
