import os
import csv
from csv import DictReader
import itertools
import pathlib2 as pathlib
import shutil

def oldPathDict(root):
    '''
    Get dictionary of all files we want to transfer
    Input- root directory
    Output- dictionary of barcode: [list of absolute paths to all files with barcode]
    Details- does not move any txt, _m, _s files. Does not specify jpg either. 
    <https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files>
    '''
    oldPathList=[]
    unwanted=["_m","_s","txt"]
    for path, subdirs, files in os.walk(root):
        for name in files:
            # Do not keep any files from unwanted list
            if any(x in name for x in unwanted):
                pass
            else:
                oldPath=os.path.join(path,name)
                oldPathList.append(oldPath)
    oldPathDictionary={}
    #turn this info into dictionary
    for oldPath in oldPathList:
        # Get file name 
        fileName=oldPath.split("/")[-1]
        barcode=fileName.split(".")[0].split("_")[0]
        #print barcode
        if barcode not in oldPathDictionary:
            oldPathDictionary[barcode]=[oldPath]
        elif barcode in oldPathDictionary:
            oldPathDictionary[barcode]=[oldPath]+oldPathDictionary[barcode]
        else:
            print("This should never happen")
    return oldPathDictionary

def portalDict(occurrencesFile,portalName,colName="catalogNumber"):
    '''
    Get dictionary of all barcodes and respective portal names
    Input - occurrences.csv, name of portal, and name of column with barcodes
    Output - Dictionary of barcodes and portal name for each barcode
    '''
    with open(occurrencesFile, "rU") as csv_file:
        catNumList = [row[colName] for row in DictReader(csv_file)]
    portalDictionary={}
    for n in catNumList:
        portalDictionary[n]=portalName
    return portalDictionary




# Get old path dictionary
oldRoot = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/'
oldPathDictionary=oldPathDict(oldRoot)

# Get portal dictionary
occurrencesFile="/Users/ChatNoir/Projects/HerbariumRA/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"
colName="catalogNumber"
portalName="bryophyte"
portalDictionary=portalDict(occurrencesFile,portalName,colName)

# Move files
newRoot='/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsuNEW/'


noImageBarcodeDict={}
alreadyExists=[]
# Iterate through barcodes that are in the specify database
for bcp in portalDictionary:
    # If barcode has image files... 
    if bcp in oldPathDictionary:
        # Split apart letters and numbers from barcode
        barcodeSplit = ["".join(x) for _, x in itertools.groupby(bcp, key=str.isdigit)]
        # Iterate through all image files associated with barcode
        for oldPath in oldPathDictionary[bcp]:
            # Grab name of file, collection (lsu,no,etc), numerical part of barcode, portal
            fileName=oldPath.split("/")[-1]
            collection=barcodeSplit[0]
            number=barcodeSplit[1]
            portal=portalDictionary[bcp]
            # Split apart barcode number to create new file path
            lastThree=number[-3:] # this isnt nessecary, just to double check things
            cutoffThree=number[:-3]
            secondFolder=cutoffThree[-3:]
            firstFolder=cutoffThree[:-3]
            # Create folders from barcode and portal information
            # ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
            newPath=os.path.join(newRoot,portal,collection,firstFolder,secondFolder,fileName)
            # Get directory path to check if folders need to be created
            newDir=os.path.dirname(newPath)
            #print(bcp,portalDictionary[bcp], collection,number,fileName)
            #print(len(number),number,firstFolder,secondFolder,lastThree)
            # Keep track of all files that already exist in destination folder. Will happen if two portals list same files.
            if os.path.exists(newPath):
                alreadyExists.append(file)
            # If file does not exist. Create path if needed. Then move/copy file to new destination
            else:
                pathlib.Path(newDir).mkdir(parents=True, exist_ok=True)
                shutil.copy2(oldPath,newPath)
                #os.rename(oldPath,newPath)
                print(newPath)
    # If barcode has no image files
    elif bcp not in oldPathDictionary:
        # keep track of specify records with no image file. 
        noImageBarcodeDict[bcp]=portalDictionary[bcp]
    


###### NOTES ##########
To Do:
- put last for loop into function 
- check for corrupted Images
- figure out what list comparisons need to be done. 


all portal barcodes should be in Images
    - list of all in Images
    - list of all NOT in Images. 

for barcode in portal 
if portal barcode NOT in allfiles
add to list - no photo for specify entry. 


moving file
no file to move (no image OR already claimed in a different portal)
already identicle file in new destination


https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python



if key from FD matches key from PD 
make new path 
newpathFolder = PD value / collection-institutionID / numbers from barcode
for value in FD_key:
    filename = get filename from oldpath value 
    check for corruption - if corrupt, add to corruption dictionary barcode:newpathfolder+filename
    move to newPath (if folders don't exist, then make them)

Flags for:
already identicle file in new destination
no file to move (already claimed in a different portal)



Images without specify entry - should be 0. output list of all barcodes that have an image on cbfla. 
    - all of these should exist in master specify list 
Specify entry without image - during each portal move, output list of all barcodes in specify with no image file barcode. 
    - these may be already moved, or just dont have an image. 
    - will need to compare this list to list of all image barcodes

root+lsu(?)+portal+collection+
nfsshare/lsu/vascular/lsu/##/###/file.jpg 
#print(noImageBarcodeDict)

nfsshare/lsu/vascular/lsu/##/###/file.jpg 
nfsshare/vascular/lsu/##/###/file.jpg

LSU01020304 -> ['01','020']
vascular/lsu/01/020/LSU01020304.jpg
vascular/lsu/00/099/LSU00099999.jpg



NO0010203 -> ['0','010']
vascular/no/0/010/NO0010203.jpg

output 
corrupted file dictionary barcode:new file path
barcode list (set) - make set from file directory keys



# Portal Dictionary. key = barcode. value = portal type
'''
Vascular Plants: http://sernecportal.org
Lichens: http://lichenportal.org
Bryophytes: http://bryophyteportal.org
Fungi: http://mycoportal.org
Algae: http://macroalgae.org
'''
occurances file - look for 'catalogNumber' user input 
