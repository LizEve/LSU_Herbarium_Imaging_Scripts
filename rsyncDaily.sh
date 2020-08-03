#!/bin/bash


# need to run this as root
# outlogs should be output to source computer log folder
# Source, destination, and logfolder MUST be folders WITH A TRAILING FORWARD SLASH

destination=/data/LSUCollections/

# Repeat for second computer - WS2 
source2=/mnt/LSUCollections/
logfolder2=/mnt/LSUCollections/Logs/
outlog2=/mnt/LSUCollections/Logs/rsync2.out # Only need one because rsync writes over it each time rsync is called
suffix2=_server_ws2.txt # adding "_server" to end of log file so it is differentiated from files sorted locally
csvfolder2=/mnt/LSUCollections/CSVLogs/

rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update --exclude '*CR2' --exclude '*Log*' $source2 $destination | grep '^>f' | cut -d' ' -f2 > $outlog2

while read g;
do
fname=`date +'%Y-%m-%d'`
echo $g >> $logfolder2$fname$suffix2
mvdPath=$destination$g
convert $mvdPath -units pixelsperinch -density 80x80 -resize 1400x1400^ -quality 80 ${mvdPath%.JPG}_WR.JPG
convert $mvdPath -units pixelsperinch -density 80x80 -resize 200x200^ -quality 80 ${mvdPath%.JPG}_TN.JPG
convert $mvdPath -quality 95 ${mvdPath%.JPG}_L.JPG
done < $outlog2

# Sync all csv files to sassafrass folder 
csvRemote=/data/LSUCollections/Logs/
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update $csvfolder2 $csvRemote 

# checking if script is running
echo $fname
echo $logfolder2$fname$suffix2

