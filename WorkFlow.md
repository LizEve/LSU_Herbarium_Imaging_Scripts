##### Still in development ####

# Imaging Workflow 

1. Turn on camera

2. Wait for EOS to open

3. Check EOS settings
   1. Confirm that `renameimage.exe` is 'registered' to EOS 
      1. Preferences > Linked Software > Register > Browse - select `renameimage.exe`
      2. Full path - `C:Users\Image\Documents\PNWHerbaria\Scripts\renameimage\renameimage.exe`

4. Select portal folder 
   1. In EOS - Preferences > Destination Folder
   2. Select one of the portal folders `C:Users\Image\Desktop\Imaging\`
   3. Personal projects and other special collections that are not going on Symbiota should be imaged in the **Random** folder if you want the images backed up to the server (Sassafrass). Any folders in **Random** will be moved as is to the local backup drive, not sorted into portal folders. 

5. Take photo 
   1. A small box should pop up with the current file name and an place to enter the new name

6. Scan barcode
   1. Barcode should appear as new file name 
   2. Click the "rename" button to rename the file 
   3. The small window will close after the file is renamed. 

Repeat 5. & 6. for all photos

7. Batch edit photos in DPP 

8. Convert from CR2 to JPG
   1. Now you are done, make sure to record on paper what specimens you imaged

Weekly 

1. Upload CSV 
   1. CSV files ready for upload are on in the CSVLogs/ folder. On workstation 2 at LSU.
   2. After uploading CSV files please move them to the CSVLogged/ folder. 
   3. If file names are edited and re-uploaded a new CSV file will be made for the date the original file was uploaded. This CSV can be combined with or replace the older CSV in the CSVLogged folder. 

## Behind the scenes

### 6PM - RunOrganize.sh, organizeIncomingImages.py, ReBoot Ubuntu

- Ubuntu gets rebooted from Task Scheduler
- Files get moved from the desktop to the LaCie
- Long form logs are written to the Desktop in the folder Desktop/Imaging/Logs/ with the extension '_organize_ws2.txt'
- Tally of files moved are appended to the file 'organizeLog.csv' in CFLA-LSU-Station2/LSUCollections/CSVLogs/
- Scripts run: RunOrganize.sh, organizeIncomingImages.py, 

### 8PM - WakeUp.sh, rsyncDaily.sh

- Wakeup script runs on workstation
- Sassafrass pulls files from LaCie using scripts on Sassafrass
- Long form logs are written in CFLA-LSU-Station2/LSUCollections/Logs/ on the LaCie with the extention '_server_ws2.txt'
- Scripts run: WakeUp.sh, rsyncDaily.sh

### 11 PM - RunCountServer.sh, CountServerLogs.py, task manager reboot ubuntu

- Use long form logs from 8PM syncing to tally the total number of files uploaded and writes the results to the file 'serverLogWS2.csv' on the LaCie in the folder CFLA-LSU-Station2/LSUCollections/Logs/
- Scripts run: RunCountServer.sh, CountServerLogs.py, task manager reboot ubuntu


### Check 
organizeLog.csv and serverLogWS2.csv should have the same number of barcodes and files per portal. Total number of files should be double in organizeLog.csv because CR2 files are counted. 

### Weekly 
- CSV files are made from the long form upload logs created in the last week. 
- The total files in each csv file are written to the file 'csvLog.csv' on the LaCie in the folder CFLA-LSU-Station2/LSUCollections/CSVLogs/
- These csv logs will also be synced to the Sassafrass log folder accessible at - https://cyberfloralouisiana.com/images/LSUCollections/Logs/
- Scripts run: LogtoCSV.py


## Scripts 

### Run on Desktop with Task Scheduler

RunOrganize.sh - runs organizeIncomingImages.py at 6PM every day. 

organizeIncomingImages.py - Checks barcodes in incoming folders, moves to appropriate folder(based on barcode) on storage drive. Put files with names that are too long or too short in BadBarcode folder. Outputs one long form log file per day with all destination file paths. Writes to master log file with number of files and barcodes moved to LaCie, also broken down by collection. Uses long form of logs to count files. This does not count files in the "Random" folder. 

WakeUp.sh - wakes up the computer to sit and wait for 13 hours at 7:55 PM, this allows the server to connect to the storage drive, in order to copy over files. 

RunCountServer.sh - runs CountUploadLogs.py at 11PM every day. 

CountServerLogs.py - Called by Task Scheduler. Writes to master log file with number of files and barcodes moved to the server, also broken down by colletion. Uses long form of log for each day to count files. This does not count files in the "Random" folder. 

RunWeeklyCSV.sh - runs LogtoCSV.py at XX every week on Saturday.

WeeklyCSV.py - Takes all rsync logs that were modified in the last week hours and creates or adds to csv files that have not been uploaded to a portal yet. 

### Run on server by crontab: 

rsyncDaily.sh - runs on server to copy files to server and create derivatives. 
Outputs one log file per day (per computer) with all destination file paths. 
Passes current day's log file to CountRsyncLogs.py to count total files/barcodes moved.
errors written to - /data/LSUCollections/Logs/dailyrsynclog.txt