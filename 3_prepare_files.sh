#find $1 -name '*.avi' | sort | grep results > /monitoreo/sdm_yolo/sdm_yolo/aforo_0.txt
# usage
# ./3_prepare_files.sh /monitoreo/videos/Videos_2022_02_17/results/
find $1 -name '*.avi' | sort | grep results > /monitoreo/sdm_yolo/sdm_yolo/tmp1.txt
exec < /monitoreo/sdm_yolo/sdm_yolo/tmp1.txt
while read line
do
  pickle_filename=$1"config.pkl"
  echo $line $pickle_filename >> tmp2.txt
done
cat tmp2.txt >> /monitoreo/sdm_yolo/sdm_yolo/aforo_0.txt
rm tmp1.txt
rm tmp2.txt
