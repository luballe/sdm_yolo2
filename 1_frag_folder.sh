#!/bin/bash
# Usage ./frag_folder.sh /path/to_files
#echo "**** Starting fragmentation of "$1" at: "$(date)
python3 /monitoreo/sdm_yolo/sdm_yolo/python/fragmentador_video_SAM_batch.py "$1" #&
echo "Deleting old avi files... "
cd $1
rm *.avi
echo "Old avi files deleted!"
echo "Done!!!"
#wait $!
