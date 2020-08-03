#!/bin/bash


# need to run this as root
# outlogs should be output to source computer log folder
# Source, destination, and logfolder MUST be folders WITH A TRAILING FORWARD SLASH

destination=/data/LSUCollections/

# Repeat for second computer - WS2 
source=/mnt/LSUCollections/
logfolder=/data/LSUCollections/Logs/
outlog=/data/LSUCollections/Logs/rsync2.out # Only need one because rsync writes over it each time rsync is called
suffix=_server_ws2.txt # adding "_server" to end of log file so it is differentiated from files sorted locally
csvfolder=/mnt/LSUCollections/CSVLogs/

rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update --exclude '*CR2' --exclude '*Log*' $source $destination | grep '^>f' | cut -d' ' -f2 > $outlog

while read g;
do
fname=`date +'%Y-%m-%d'`
echo $g >> $logfolder$fname$suffix
mvdPath=$destination$g
convert $mvdPath -units pixelsperinch -density 80x80 -resize 1400x1400^ -quality 80 ${mvdPath%.JPG}_WR.JPG
convert $mvdPath -units pixelsperinch -density 80x80 -resize 200x200^ -quality 80 ${mvdPath%.JPG}_TN.JPG
convert $mvdPath -quality 95 ${mvdPath%.JPG}_L.JPG
done < $outlog

# Sync all csv files to sassafrass folder 
csvRemote=/data/LSUCollections/Logs/
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update $csvfolder $csvRemote 

# checking if script is running
echo $fname
echo $logfolder$fname$suffix

