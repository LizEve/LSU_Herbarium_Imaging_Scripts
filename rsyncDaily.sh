#!/bin/bash


# need to run this as root
# outlogs should be output to source computer log folder
# Source, destination, and logfolder MUST be folders WITH A TRAILING FORWARD SLASH



# Set custom extension for log file names
suffix=_server_ws2.txt # adding "_server" to end of log file so it is differentiated from files sorted locally

# Set custom folders 
# Where the image files are coming from and going to
source=/mnt/LSUCollections/
destination=/data/LSUCollections/

# Where the log files are written to and the temporary daily log file
logfolder=/data/LSUCollections/Logs/server_ws2_logs/
outlog=/data/LSUCollections/Logs/server_ws2_logs/rsync2.out 

# Where the log files get moved to for further counting and processing
wsLogs=/mnt/LSUCollections/Logs/

# Workstation and server csv folders for syncing 
csvfolder=/mnt/LSUCollections/CSVLogs/
csvRemote=/data/LSUCollections/Logs/


# Name today's log after the date
fname=`date +'%Y-%m-%d'`
todaylog=$logfolder$fname$suffix

# print date so i can see how long rsync takes 
echo "starting rsync"
date +"%T"

rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update --exclude '*CR2' --exclude '*Log*' $source $destination | grep '^>f' | cut -d' ' -f2 > $outlog

echo "starting file resizing"
date +"%T"

while read g;
do
echo $g
echo $g >> $todaylog
mvdPath=$destination$g
convert $mvdPath -units pixelsperinch -density 80x80 -resize 1400x1400^ -quality 80 ${mvdPath%.JPG}_WR.JPG
convert $mvdPath -units pixelsperinch -density 80x80 -resize 200x200^ -quality 80 ${mvdPath%.JPG}_TN.JPG
convert $mvdPath -quality 95 ${mvdPath%.JPG}_L.JPG
done < $outlog

echo "starting log copy"
date +"%T"

# Copy logs to workstation 
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update $logfolder $wsLogs 


# Sync all csv files to sassafrass folder 
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update $csvfolder $csvRemote 

# checking if script is running
echo $fname
echo $todaylog

