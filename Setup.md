
# Setup of Imaging Pipeline

## General 

### Acronyms 

DPP - Digital Photo Professional
EOS - EOS Utility - a program to conect computer to camera

### Programs/versions

Python3 and package downloader like pip. 
Ubuntu XXX
Computer with Windows 10
Local backup drives plugged into or mounted on the windows machines. 
Remote server for long term storage and serving images. 

### System Requirements 

These scripts have been tested using Windows 10 and Ubuntu XXX. All scripts should work on any linux platform. However, the automation of running scripts daily will be different. 

## Download and edit scripts on imaging computer

### renameimage.exe - renaming image files 

#### Download

- `http://www.pnwherbaria.org/documentation/specimenimaging.php`
- Scroll down and click on **Imaging Computer Configuration** to download.  
- This will download a whole folder that is a different imaging pipeline. We only need the script `renameimage.exe` in the folder `PNWHerbaria\Scripts\renameimage\`

#### Store locally 

- Put this script somewhere it is easy to find and hard to edit or move. It should stay in the same place forever. 

    ex: LSU `C:Users\Image\Documents\PNWHerbaria\Scripts\renameimage\renameimage.exe`

#### Link `renameimage.exe` to EOS

- EOS needs to link directly to `renameimage.exe`, so that when a photograph is taken, EOS passes the default file name to `renameimage.exe`. For each photo taken `renameimage.exe` will open and provide a window to rename the file manually or with a barcode reader.
- Open EOS - Preferences > Linked Software > Register > Browse
  - Click **Preferences**
  - Click **Linked Software**
  - Click **Register**
  - Click **Browse** and link to `renameimage.exe`

### organizeIncomingImages.py - organize and move image files

#### Function 

Running `organizeIncomingImages.py` will do the following-

- Each file will be checked for the appropriate barcode format and length. 
- Files with inaccurate barcodes will be placed in a folder called `BadBarcode` in the source folder provided to the script. These file names will need to be manually edited and placed in the appropriate portal folders in the source folder. 
- Accurate barcodes will be moved to the destination folder, which should be on an external harddrive or other backup. 
- As files are moved to the destination/backup drive they will be filed based on their barcode and which source folder they are found in. 

#### Log files

- Output logs based on date created, or on date modified if creation date cannot be identified, a potential on linux machines. 
- If the source folders have images in them, a log will be written for that day. 
- Each log will be named based on the date with the option to add an additional string of letters or numbers. 
- For LSU the log names will contain the date and the computer they are imaged on. `date_workstation1` 
- Be careful when re-editing photos in DPP after the day they are taken, this may cause their log date to change on the server sync logs.

#### File name restrictions

- File names are expected to start with a barcode. This barcode should start with letters followed by ONLY numbers.
- Extra notes or tags, such as numbering multiple files should come after an underscore "_" 
  - Ex: LSU01234567.JPG or LSU01234567_1.JPG
- All file names will be changed to all caps if they are not already. Except those files in the other/random folders
- Folders will be created first using the letters, then using the numbers. Ex: /LSU/001/002/
- **BadBarcode Folder** : Files with improperly formatting barcodes will be sent here. Edit file names in this folder and place in appropriate source folder so they will be uploaded properly. 
- When barcode/filename is fixed, the file will be recorded in the log coresponding to the day the file was originally created. If you edit the file in DPP again the server logs may record the file as originating from the day you re-edited the photo. Make sure to record this in any paper logs.
  
#### Download

- `https://github.com/LizEve/HerbariumRA.git`
- Click blue button **Clone or download**
  - Click **DownloadZIP**

#### Store locally

- Again put this folder somewhere it is easy to find and hard to edit or move.
    ex: LSU `C:Users\Image\Documents\GitHub\HerbariumRA`

#### Edit script 

- `organizeIncomingImages.py` needs to be customized to your computer 
- Open python script in a simple text editor like NotePad, NOT microsoft word. 
- Scroll down to the bottom of the file under `def main():` and edit the following variables:

**sourceFolder** - Folder of images on computer `/mnt/c/Users/Image/Desktop/Imaging/`

**destinationFolder** - Folder for long term storage `/mnt/e/CFLA-LSU-Station2/LSUCollections/`

**portalFolders** - List of folders that correspond to how you want to store your images. These will be automatically created if they don't already exist. `['Algae','Bryophyte','Fungi','Lichen''Vascular']`

**otherFolders** - Extra folders for one time projects. Barcodes will not be checked, and any nested folders will be moved as is. These will be automatically created if they don't already exist. `['Random']`

**barcodeMax/Min** - Maximum and minimum length for legitimate barcode, does not count anything trailing an underscore "_" `15` `9`

### Set up auto run of organizeIncomingImages.py

- Use this tutorial to set up the task to run every day. 
- `https://www.thewindowsclub.com/wake-up-computer-from-sleep-windows`
- Ex LSU - Run at 7PM `wsl python3 /mnt/c/Users/Image/Documents/GitHub/HerbariumRA/organizeIncomingImages.py` 

## Server

### Mount local backups to remote server

Mount local backups onto server. Google or get help from departmental IT.

### Download and edit rsyncDaily.sh

#### Download and store

- `https://github.com/LizEve/HerbariumRA.git`
  - Copy script from imagining computer or use github to clone 
- Store script somewhere that is executable by root. 
  
#### Functions and edits

- This script will copy files from local backup to remote server 
  - Currently CR files are excluded from this copy. 
- Edit source, destination, log folder, and log file names 
  - Destination folder is the folder on the server that you are syncing the files to. 
  - Source folder is the path to the mounted local backups
  - Log folder and log file names can be customized. 
    - LSU log files are written to backup drives for easy comparison to logs of which files are moved. 
- Edit rsync call if needed 
  - Current rsync call is custom for LSU. It changes permissions of the files when they are moved to match the permissions for our server. This includes a custom user group called 'adm'.
  
### Set up cron job for rsyncDaily.sh 

- Cron info - https://www.adminschoice.com/crontab-quick-reference
- Recomend running as root to avoid any file writing or permissions issues. 
- Add rsyncDaily.sh to cron jobs 
  - Open root crontab for editing `sudo crontab -u root -e`
  - Run at 10:15 PM every day. `15 22 * * * /bin/sh /var/www/rsyncDaily.sh &> /data/LSUCollections/Logs/dailyrsynclog.txt`
- Had to change some permissions so that when root writes to the log folder, the permissions stay the same as the rest of the /data/ folder. `sudo vim /etc/logrotate.d/apache2 rsyncDaily.sh`

### Set wake up for imaging wcomputers 

- Set up workstations to wake up before rsync script is scheduled to start. 
- Make sure the sleep setting is longer than the time you set between waking them up and running the rsync script. 
Again use task scheduler - `https://www.thewindowsclub.com/wake-up-computer-from-sleep-windows`


### Rsync logs

- Files are written to output logs based on date modified. Modification date is the last time the contents of the file were altered, simply renaming the file itself should not change the modification date. 
- File creation date is complicated to aquire on Linux machines, so I am using modification date which should server our purposes.
- Rsync logs are similar to the organizing logs. They are named based on the date and a trailing custom string. 
- For LSU the log names will contain the date, the word 'server' to indicate they are logs for server upload, and the computer they are imaged on.


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


