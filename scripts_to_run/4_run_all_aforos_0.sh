#!/bin/bash
# Usage:
# ./4_run_all_aforos_0.sh /monitoreo/videos/Videos_2022_02_17/0700-1000-CR10x19_NS/config.pkl 
function run {
 echo started "$1" : $(date)
 ./3_2_aforo_0.sh "$1" "$pickle_file" &
 echo Done "$1" : $(date)
}


num_gpu_processors=4
#pickle_file="/monitoreo/videos_Ago09_Ago13/128_config.pkl"
pickle_file=$1
videos_list_file=$2
exec < $videos_list_file
while read line
do
  while [ $(ps -a | grep 3_2_aforo | wc -l) -ge $num_gpu_processors ]
  do
    sleep 10s
  done
  sleep 2s
  run "$line"
done


