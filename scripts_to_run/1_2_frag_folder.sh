#!/bin/bash
# Usage ./frag_folder.sh /path/to_files
#echo "**** Starting fragmentation of "$1" at: "$(date)
python3 /monitoreo/sdm_yolo/sdm_yolo/python/fragmentador_video_SAM_batch.py "$1" &
wait $!
