#find /monitoreo/videos_Ago09_Ago13/ -type f -name '*.avi' | sed -r 's|/[^/]+$||' | sort | uniq | grep KR128

# Usage:
# ./1_1_populate_input_folder_list.sh /monitoreo/videos/Videos_2022_02_17
find $1 -type f -name '*.avi' | sed -r 's|/[^/]+$||' | sort | uniq > /monitoreo/sdm_yolo/sdm_yolo/folders_to_frag.txt
