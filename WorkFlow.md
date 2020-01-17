##### Still in development ####

# Imaging

## Turn on camera

### Wait for EOS to open

### Select portal folder to deposit images into 

In EOS- Preferences > Destination Folder

## Take Photos

### Scan barcode 

Add notes about how the new renaming script works. And where it lives. And where to find it and download and put it if anything happens. 

## Open DPP

### Batch edit 

### CR to jpg

## Now you are done, make sure to record on paper what specimens you imaged

## Move images from Desktop to Backup 

### On initial setup 

#### Retrieve scripts \*setup\*

##### Rename Script

Link - `http://www.pnwherbaria.org/documentation/specimenimaging.php`
- Scroll down and click on `Imaging Computer Configuration` to download.  

Local storage of script - `\PNWHerbaria\Scripts\renameimage\renameimage.exe`

Open EOS - Preferences > Linked Software > Register > Browse
`C:Users\Image\Documents\PNWHerbaria\Scripts\renameimage\renameimage.exe`

##### Reorganize Script

Github link - `https://github.com/LizEve/HerbariumRA.git`

Local storage of script `/mnt/c/Users/Image/Documents/GitHub/HerbariumRA`  

#### Edit script \*setup\*

**sourceFolder** - Folder of images on computer `/mnt/c/Users/Image/Desktop/Imaging/`

**destinationFolder** - Folder for long term storage `/mnt/e/CFLA-LSU-Station2/LSUCollections/`

**portalFolders** - List of folders that correspond to how you want to store your images. These should exist in both the source and destination folder. `['Algae','Bryophyte','Fungi','Lichen''Vascular']`

**otherFolders** - Extra folders for one time projects. Barcodes will not be checked, and any nested folders will be moved as is. These should exist in both the source and destination folder. `['Random']`

**barcodeMax/Min** - Maximum and minimum length for legitimate barcode, does not count anything trailing an underscore "_" `15` `9`

### Auto run organzing script \*setup\* 

`https://www.thewindowsclub.com/wake-up-computer-from-sleep-windows`

From task scheduler 
Run at 7PM `wsl python3 /mnt/c/Users/Image/Documents/GitHub/HerbariumRA/organizeIncomingImages.py` 

might be similar to this - https://www.thewindowsclub.com/wake-up-computer-from-sleep-windows

### Additional notes on organizeIncomingImages.py

#### File name restrictions

- File names are expected to start with a barcode. This barcode should start with letters followed by ONLY numbers.
- Extra notes or tags, such as numbering multiple files should come after an underscore "_" 
  - Ex: LSU01234567.JPG or LSU01234567_1.JPG
- All file names will be changed to all caps if they are not already. Except those files in the other/random folders
- Folders will be created first using the letters, then using the numbers. 

## Daily Organize

At 6PM the script organizeIncomingImages.py is programed to run using XXX. No user input is needed at this point. 

Each file will be checked for the appropriate barcode format and length. Files with inaccurate barcodes will be placed in a folder called `BadBarcode` in the source folder provided to the script. These file names will need to be manually edited and placed in the appropriate portal folders in the source folder. 
Accurate barcodes will be moved to the destination folder, which should be on an external harddrive or other backup. As files are moved to the destination/backup drive they will be filed based on their barcode and which source portal folder they are found in. For more details see the above setup notes or in organizeIncomingImages.py. 

### BadBarcode 

Edit file names in this folder and place in appropriate portal folder. They will be recorded as moved on the date they were originally taken. **If you edit the file in DPP again** the server logs may record the file as originating from the day you re-edited the photo. Make sure to record this in any paper logs.


### Logs 

Output logs based on date created, or on date modified if creation date cannot be identified, a potential on linux machines. 
If the source folders have images in them, a log will be written for that day. Each log will be named based on the date with the option to add an additional string of letters or numbers. For LSU the log names will contain the date and the computer they are imaged on. `date_workstation1` 
Be careful when re-editing photos in DPP after the day they are taken, this may cause their log date to change on the server sync logs. 

## Server 

### Setup \*setup\*

Mount backups onto server 

#### Edit rsyncDaily.sh \*setup\*

Edit source, destination, log folder, and log file names 
- SoDestination = folder on the server that you are syncing the files to. 
- Log folder and file names = custom. 
  - LSU will write log files to the backup drives so they can be easily compared with the logs that record when files were originally moved from the imagine computer to the backup. 

Edit rsync call if needed 
- The actual rsync call is somewhat custom for LSU. It changes permissions of the files when they are moved to match the permissions for our server. This includes a custom user group called 'adm'. We also do not upload original CR2 images. 

#### Cron job \*setup\*

Add rsyncDaily.sh to cron jobs
Recomend running as root to avoid any file writing or permissions issues. LSU will send error logs to one of the backup drives so they are easily accessible. 
Cron info - https://www.adminschoice.com/crontab-quick-reference

#### Setup cron job for root \*setup\*

Open root crontab for editing `sudo crontab -u root -e`

Run at 10:15 PM every day. `15 22 * * * /bin/sh /var/www/rsyncDaily.sh &> /data/LSUCollections/Logs/dailyrsynclog.txt`

Write log to file that is accessible from web. Can't write to mounted drives. 
15 22 * * * /bin/sh /var/www/rsyncDaily.sh &> /data/LSUCollections/Logs/dailyrsynclog.txt

Had to change some permissions so that when root writes to the log folder, the permissions stay the same as the rest of the /data/ folder. `sudo vim /etc/logrotate.d/apache2 rsyncDaily.sh`

### Daily Sync

#### Wake up workstation computers 

Set up workstations to wake up before rsync script is scheduled to start. Make sure the sleep setting is longer than the time you set between waking them up and running the rsync script. 

https://www.thewindowsclub.com/wake-up-computer-from-sleep-windows

#### Rsync via rsyncDaily.sh

Moves files from mounted backup drives.
Changes permissions to match what LSU has set up for our image folders.
Write log files to work stations Log folder, ex: `/mnt/LSUCollections/Logs/`


##### Rsync logs

Files are written to output logs based on date modified. Modification date is the last time the contents of the file were altered, simply renaming the file itself should not change the modification date. File creation date is complicated to aquire on Linux machines, so I am using modification date which should server our purposes.
Rsync logs are similar to the organizing logs. They are named based on the date and a trailing custom string. For LSU the log names will contain the date, the word 'server' to indicate they are logs for server upload, and the computer they are imaged on.


## TO DO after xyz 

- enable rsync after QC on WS2 and WS1, and after WS1 box upload. 
- set up actual rsync after WS1 is all on synology and then all on box 

## Tail ends of things to wrap up? 

- clean up computers - genna 
- add extras to WS1 synology - genna 
- Edit permissions on synology? - eric 

## Additional set up notes 

### Windows 10

#### Install Ubuntu 18.04 LTS

Install from Microsoft Store

#### Mount network drives in Ubuntu 

`https://docs.microsoft.com/en-us/archive/blogs/wsl/file-system-improvements-to-the-windows-subsystem-for-linux`


