#!/bin/bash
# Usage:
# ./4_run_all_aforos_0.sh  
function run {
# echo started "$1" : $(date)
 ./4_1_aforo_0_sentidos.sh "$1" "$2" "$3" &
# echo Done "$1" : $(date)
}


num_gpu_processors=4
#pickle_file="/monitoreo/videos_Ago09_Ago13/128_config.pkl"
#pickle_file=$1
#videos_list_file=$2
videos_list_file="/monitoreo/sdm_yolo/sdm_yolo/aforo_0.txt"
num_files=0
exec < /monitoreo/sdm_yolo/sdm_yolo/aforo_0.txt
while read line
do
  num_files=$((num_files+1))
done
echo "Num files:"$num_files

i=1
exec < $videos_list_file
while read line
do
  while [ $(ps -a | grep 4_1_aforo | wc -l) -ge $num_gpu_processors ]
  do
    sleep 10s
  done
  sleep 2s
  run "$line" "$num_files" "$i"
  i=$((i+1))
done


