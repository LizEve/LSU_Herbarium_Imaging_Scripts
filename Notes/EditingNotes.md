# Notes on what scripts get edited 

Last update - 10.30.20

## Rename output csv and txt files 

organizeimages
    outLogsuffix="local_ws2.txt"
    
    csvFolder='/mnt/c/Users/Image/Desktop/Imaging/LocalLogs/'
    
    csvLogFilePath = os.path.join(csvFolder,'DailyLocalLog.csv')


## Rename scripts 

organize - local move
rsync - move to server 
etc

## Simplify workflow notes 

Images folder -> LaCie drive 9PM
Output - Imaging/LocalLogs
Create single log with daily file list (_local_ws2.txt)
Add file count to DailyLocalLog.csv

LaCie drive -> Sassafras 10PM
Output - Server - /data/LSUCollections/Logs/DailyWS2/
Create single log with daily file list (_server_ws2.txt)
Moves daily file lists to Local - /mnt/LSUCollections/ServerLogs/

Count server files 11PM 
In LaCie drive - LSUCollections/ServerLogs/
Add file count to - DailyServerLogWS2.csv
