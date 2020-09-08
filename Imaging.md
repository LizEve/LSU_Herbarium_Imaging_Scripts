# Imaging Workflow 
https://github.com/LizEve/LSU_Herbarium_Imaging_Scripts

1. Turn on camera

2. Wait for EOS to open

3. Check EOS preferences
   1. Confirm that `renameimage.exe` is 'registered' to EOS 
      1. Preferences > Linked Software > Register > Browse - select `renameimage.exe`
         a. Make sure "CR2" is checked 
      2. Full path - `C:Users\Image\Documents\PNWHerbaria\Scripts\renameimage\renameimage.exe`

4. Select portal folder 
   1. In EOS - Preferences > Destination Folder
   2. Select one of the portal folders `C:Users\Image\Desktop\Imaging\`
   3. Personal projects and other special collections that are not going on Symbiota should be imaged in the **Random** folder if you want the images backed up to the server (Sassafrass). Any folders in **Random** will be moved as is to the local backup drive, not sorted into portal folders. 

5. Open DPP in Imaging folder `C:Users\Image\Desktop\Imaging\`
   1. Filter on 

6. Take photo 
   1. A small box will pop up with the current file name and a place to enter the new name

7. Scan barcode
   1. Barcode should appear as new file name - edit with _1 or other number if needed
   2. Click the "rename" button to rename the file 
   3. The small window will close after the file is renamed. If needed you can edit the names later in DPP

Repeat 5. & 6. for all photos

8. Batch edit photos in DPP 
   - if needed, can rename files in DPP using the barcode scanner

9. Convert from CR2 to JPG
   1. Now you are done, make sure to record on paper what specimens you imaged


   Weekly 

1. Upload CSV 
   1. CSV files ready for upload are on in the CSVLogs/ folder. On workstation 2 at LSU.
   2. After uploading CSV files please move them to the CSVLogged/ folder. 
   3. If file names are edited and re-uploaded a new CSV file will be made for the date the original file was uploaded. This CSV can be combined with or replace the older CSV in the CSVLogged folder. 

Log Files 

Logs for files transfered from Imaging to LaCie Drive 
- Daily lists of files are in Desktop/Imaging/Logs/ with the extension '_organize_ws2.txt'
- Daily counts of files are in Desktop/Imaging/Logs/organizeLog.csv

Logs for files transfered from LaCie Drive to Sassafras Server 
- Daily lists of files are in CFLA-LSU-Station2/LSUCollections/Logs/ on the LaCie with the extention '_server_ws2.txt'
- Daily counts of files are in CFLA-LSU-Station2/LSUCollections/Logs/serverLogWS2.csv

The total number of barcodes should match between organizeLog.csv and serverLogWS2.csv. The number of files will be doubled in organizeLog.csv because it counts both JPG and CR2 files. 

