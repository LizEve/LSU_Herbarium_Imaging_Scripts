#!/bin/bash

# run once a day right before cyberflora patch moves everything 
# if txt file contains any lines. 
# move to log folder with name that will match moving folder thinger. 
# Move_incoming_log.sh
x=`cat /data_storage/cfla/filesmovedtoday.txt  | wc -l`
if [ "$x" -gt 0 ]
then
mv /data_storage/cfla/filesmovedtoday.txt "/data_storage/nfsshare/incoming_logs_2018/$(date +"%Y_%m_%d")_incomingfiles.out"
fi

