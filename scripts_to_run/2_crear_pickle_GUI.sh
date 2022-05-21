#!/bin/bash
# Usage: 2_crear_pickle.sh /path/to_files EW,WE,NS,SN
# ./2_crear_pickle.sh /monitoreo/videos_Ago09_Ago13/Ago09/09-08-2021/CL13xKR128/0600-0700/ 128_WE,128_EW,128_ciclo_WE,12_ciclo_EW

# ./2_crear_pickle.sh /path/to_files "/monitoreo/videos/0600_0800" 1
pwd_cmd='pwd'
current_path=$(eval "$pwd_cmd")'/'
#folder="/monitoreo/Aforos_CGT/2020_06_12/1_AK 7 X AC 72/0600_0800"
folder="$1"
sentidos="$2"
cd /monitoreo/sdm_yolo/sdm_yolo/python
python2 Crear_pickle.py "$folder" $sentidos
#cd "$folder"
#mkdir "results"
#cp "config.pkl" "results"
#cd ..
#mkdir -p "1100_1400/results"
#cp "0600_0800/config.pkl" "1100_1400/results"
#mkdir -p "1700_1900/results"
#cp "0600_0800/config.pkl" "1700_1900/results"

#cd $current_path
