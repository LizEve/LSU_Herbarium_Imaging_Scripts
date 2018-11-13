import os
import csv
from csv import DictReader
import itertools
import pathlib2 as pathlib
import shutil
from PIL import Image

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
        # Ignore hidden directories as files, those that start with "."
        files = [f for f in files if not f[0] == '.']
        subdirs[:] = [d for d in subdirs if not d[0] == '.']
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

def moveFiles(newRoot,oldPathDictionary,portalDictionary):
    '''
    Organizes files based on barcode and portal. 
    Input - New parent folder. Dictionary of old paths. Dictionary of barcodes and their portal
    Output - Dictionary of files moved {filename:[barcode,portal,newpath]}. 
    Dictionary of barcodes with no image {barcode:portal}
    '''
    # filename:[barcode,portal,newpath]
    filesMovedDict={}
    # barcode:portal
    barcodeNoImageDict={}
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
                # If file does not exist. Create path if needed. Then move/copy file to new destination
                if not os.path.exists(newPath):
                    pathlib.Path(newDir).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(oldPath,newPath)
                    #os.rename(oldPath,newPath)
                    filesMovedDict[fileName]=[bcp,portal,newPath]
                    #print(newPath)
        # If barcode has no image files
        elif bcp not in oldPathDictionary:
            # keep track of specify records with no image file. barcode:portal
            barcodeNoImageDict[bcp]=portalDictionary[bcp]
    return filesMovedDict,barcodeNoImageDict


def dictToBigList(filesMovedDict):
    '''
    Turns dictionary of filename:[barcode,portal,newpath] into continuous list of all newpaths
    '''
    # Make one single list of all image files
    allFilesList=[]
    for paths in filesMovedDict.values():
        allFilesList.append(paths[2])
    return allFilesList

def corruptImageFinder(allFilesList):
    '''
    Takes list of all absolute paths to files. Checks for image, and corruption. 
    Returns list of non image files, and list of corrupt image files
    '''
    # List of files that cannot open as an image
    noImageList=[]
    # List of files that cannot load as an image, are corrupted
    corruptImageList=[]

    for f in allFilesList:
        # Try opening image. 
        try:
            v_image = Image.open(f)
            # Try loading image
            try:
                    x=v_image.load()
            # If image cannot load, it is corrupted    
            except Exception as e:
                    corruptImageList.append(f)
                    #print(str(e)+f)
        # If image doesnt open as an image, take note
        except IOError as i:
                noImageList.append(f)
                #print(str(i)+f)
    return noImageList,corrurptImageList

# Specify full path of current parent folder of images
oldRoot = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/'

# Get dictionary of current image paths for each barcode
# barcode:[filepath1,...filepathN]
oldPathDictionary=oldPathDict(oldRoot)

# Specify full path to DwC-A occurences.csv file downloaded from portal, name of portal, column name for barcodes in occurences.csv
occurrencesFile="/Users/ChatNoir/Projects/HerbariumRA/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"
portalName="bryophyte"
colName="catalogNumber"

# Get dictionary of barcodes and their portal
# barcode:portal
portalDictionary=portalDict(occurrencesFile,portalName,colName)

# Specify full path of the new parent folder for images
newRoot='/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsuNEW/'

# Move files and keep track of files that were moved, and barcodes that don't have images 
filesMovedDict,barcodeNoImageDict=moveFiles(newRoot,oldPathDictionary,portalDictionary)

# Get list of all new image paths
newPathList = dictToBigList(filesMovedDict)

# Get lists of images with issues
noImageList,corrurptImageList = corruptImageFinder(allFilesList)

# CHECK FOR CORRUPT FILES SOMEWHERE 

###### NOTES ##########
To Do:
- check for corrupted Images
- determine what lists are output, make notes 
- figure out what list comparisons need to be done. 

- figure out what to output for sql database. 
- figure out how to update sql database on a regular basis (probably separate script)


https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python



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


# Portal Dictionary. key = barcode. value = portal type
'''
Vascular Plants: http://sernecportal.org
Lichens: http://lichenportal.org
Bryophytes: http://bryophyteportal.org
Fungi: http://mycoportal.org
Algae: http://macroalgae.org
'''
occurances file - look for 'catalogNumber' user input 
