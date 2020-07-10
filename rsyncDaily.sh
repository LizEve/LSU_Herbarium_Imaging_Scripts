#!/bin/bash


# need to run this as root
# outlogs should be output to source computer log folder
# Source, destination, and logfolder MUST be folders WITH A TRAILING FORWARD SLASH

destination=/data/LSUCollections/


source1=/mnt/LSUCollectionsWS1/
logfolder1=/mnt/LSUCollectionsWS1/Logs/
outlog1=/mnt/LSUCollectionsWS1/Logs/rsync1.out # Only need one because rsync writes over it each time rsync is called
suffix1=_server_ws1.txt # adding "_server" to end of log file so it is differentiated from log files sorted locally
# verbose and itemize changes, change ownership of moved files to match /data/
# don't move CR2 files
# pipe parses file paths that are moved 
# writes destination file paths to an outlog that is overwritten each day
# From this outlog the modification date and file name are grabbed 
rsync -avi -og --chown=root:adm --chmod=ug=rwx,o=r --update --exclude '*CR2' --exclude '*Log*' $source1 $destination | grep '^>f' | cut -d' ' -f2 > $outlog1

# File names are put into dated output logs based on the date of log written. 
# from the rsync outlog
# get the time of last modification of each file
# parse out year,month,date and write file path to that file.
# create image derivatives
# Get full path to original file and resize 
while read g; 
do
fname=`date +'%Y-%m-%d'`
echo $g >> $logfolder1$fname$suffix1
mvdPath=$destination$g
convert $mvdPath -units pixelsperinch -density 80x80 -resize 1400x1400^ -quality 80 ${mvdPath%.JPG}_WR.JPG
convert $mvdPath -units pixelsperinch -density 80x80 -resize 200x200^ -quality 80 ${mvdPath%.JPG}_TN.JPG
convert $mvdPath -quality 95 ${mvdPath%.JPG}_L.JPG
done < $outlog1


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