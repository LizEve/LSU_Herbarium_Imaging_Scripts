import os
import shutil 

file name and mod date dict 
cd source folder 
for portalfolder in source folder list:
    for file in portalfolder
        get file name 
        get mod date 

        if portalfolder != random:
            check barcode 
            if barcode good:
                get full old path
                create full new path - with uppercase file name
                try to force move from old to new:
                    append file path to text file with mod date and workstation number 
                if doesnt move:
                    append old path to an error log named by date_wontmove
            else:
                make new path to badbarcode folder 
                old path = get full path for file name 
                try force move to bad barcode. 
                    if i cant, append old path to an error log named by date_wontmove
        elif portalfolder == random:
            get all path that follows random - split 
            create new full path using file name AND folders - with uppercase file name
            move to new path, create folders as needed. 

                
Next - 
 add output file recording
 dont record files that get put in badbarcode, do record random files 
 check sassafrass for log file examples. i think ive done this already there. 
 check notes for where i was in all this 

# keep barcode folder local 

# one list of files moved to local drive
# one list of files rsynced from local drive 


DeBugging
import shutil
sourceFilePath='/mnt/c/Users/Image/Desktop/Imaging/Algae/img5650334.jpg.CR2'
destinationFilePath='/mnt/e/CFLA-LSU-Station2/Test/Algae/IMG/5/650/IMG5650334.JPG.CR2'
shutil.move(sourceFilePath,destinationFilePath)
 

folderPath='/Users/ChatNoir/Projects/HerbariumRA/HerbariumRA/Compost'
destinationFolder='/Users/ChatNoir/Projects/HerbariumRA/test/'
d = shutil.move(folderPath,destinationFolder,copy_function = shutil.copytree)