#!/bin/bash

exec < folders_to_frag.txt
while read line
do
  ./1_2_frag_folder.sh "$line"
done


