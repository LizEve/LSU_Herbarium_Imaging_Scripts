#!/bin/bash
# run this every half hour to keep incoming folder clean 
DIR='/home/silverimageftp/incoming/'
if [ "$(ls -A $DIR)" ] 
then
    # Print list of all files moved today 
    find /home/silverimageftp/incoming/LSU*  -printf '%t %f \n' >> /data_storage/cfla/filesmovedtoday.txt
    # Move files 
    mv /home/silverimageftp/incoming/LSU* /data_storage/cfla/incoming_GGMpatch2019/
fi
# sudo sh -c "find /home/silverimageftp/incoming/LSU*  -printf '%t %f \n' >> /data_storage/cfla/filesmovedtoday.txt"
#%t File's last modification time in the format returned by the C 'ctime' function.


# write another command to move and rename files moved each day at midnight, 
# if txt file contains any lines. 
# move to log folder with name that will match moving folder thinger. 
# Move_incoming_log.sh
