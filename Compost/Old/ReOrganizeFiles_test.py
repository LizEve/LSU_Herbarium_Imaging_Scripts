import os
import csv
from csv import DictReader
import itertools
import pathlib2 as pathlib
import shutil
from PIL import Image
import pandas as pd

def oldPathDict(roots):
    '''
    Get dictionary of all files we want to transfer
    Input- root directory
    Output- dictionary of barcode: [list of absolute paths to all files with barcode]
    Details- does not move any txt, _l, _m, _s, CR2 files. Does not specify file extension
    <https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files>
    '''
    oldPathList=[]
    oldPathDictionary={}
    unwanted=["_m","_s","txt","_l","CR2"]
    for root in roots:
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
    #turn this info into dictionary barcode:all filepaths with barcode
    for oldPath in oldPathList:
        # Get file name and barcode
        fileName=oldPath.split("/")[-1]
        barcode=fileName.split(".")[0].split("_")[0]
        #print barcode
        # if barcode isnt in the dictionary, add it with file, if it is, add any extra files. 
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
    # return an all caps dicts
    return portalDictionary

def newPathNames(bcp,oldPath,barcodeSplit,portalDictionary,portalName):
    '''
    Use old path to image, and portal to create a new path to place images. 
    '''
    # Grab name of file, collection (lsu,no,etc), numerical part of barcode, portal
    fileName=oldPath.split("/")[-1]
    collection=barcodeSplit[0]
    number=barcodeSplit[1]
    # Split apart barcode number to create new file path
    lastThree=number[-3:] # this isnt nessecary, just to double check things
    cutoffThree=number[:-3]
    secondFolder=cutoffThree[-3:]
    firstFolder=cutoffThree[:-3]
    # Create folders from barcode and portal information
    # ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
    newPath=os.path.join(newRoot,portalName,collection,firstFolder,secondFolder,fileName.upper())
    # Get directory path to check if folders need to be created
    newDir=os.path.dirname(newPath)
    #print(bcp,portalDictionary[bcp], collection,number,fileName)   
    #print(len(number),number,firstFolder,secondFolder,lastThree)
    # If file does not exist. Create path if needed. Then move/copy file to new destination
    return newDir,newPath,fileName.upper()

def moveFiles(newRoot,oldPathDictionary,portalDictionary,portalName):
    '''
    Organizes files based on barcode and portal. 
    Input - New parent folder. Dictionary of old paths. Dictionary of barcodes and their portal
    Output - Dictionary of files moved {filename:[barcode,portal,newpath]}. 
    Dictionary of barcodes with no image {barcode:portal}
    '''
    # Make all keys(barcodes) into uppercase. values(list of paths) will stay as is. 
    oldDictionary_BCcaps = dict((k.upper(), v) for k, v in oldPathDictionary.items())
    # filename:[barcode,portal,newpath]
    filesMovedDict={}
    # barcode:portal
    barcodeNoImageDict={}
    # Iterate through barcodes that are in the portal database
    for bcp in portalDictionary:
        # If barcode has image files... 
        if bcp in oldDictionary_BCcaps:
            # Split apart letters and numbers from barcode
            barcodeSplit = ["".join(x) for _, x in itertools.groupby(bcp, key=str.isdigit)]
            # Iterate through all image files associated with barcode
            for oldPaths in oldDictionary_BCcaps[bcp]:
                for oldPath in [oldPaths]:
                    newDir,newPath,fileName=newPathNames(bcp,oldPath,barcodeSplit,portalDictionary,portalName)
                    if not os.path.exists(newPath):
                        pathlib.Path(newDir).mkdir(parents=True, exist_ok=True)
                        shutil.copy2(oldPath,newPath)
                        #os.rename(oldPath,newPath)
                        filesMovedDict[fileName]=[bcp,portalName,newPath]
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
    Returns a dictionary of file name: file path. for all corrupted/non image files
    '''
    # Dictionary of files that cannot open as an image
    notImageDict={}
    # Dictionary of files that cannot load as an image, are corrupted
    corruptImageDict={}

    for f in allFilesList:
        # Try opening image. 
        try:
            v_image = Image.open(f)
            # Try loading image
            try:
                    x=v_image.load()
            # If image cannot load, it is corrupted    
            except Exception as e:
                    corruptImageDict[os.path.basename(f)]=f
                    #print(str(e)+f)
        # If image doesnt open as an image, take note
        except IOError as i:
                corruptImageDict[os.path.basename(f)]=f
                #notImageDict[os.path.basename(f)]=f
                #print(str(i)+f)
    return corruptImageDict

def main(oldRoots,newRoot,outFolder,occurrencesFile,portalName,colName):

    # Get dictionary of current image paths, organized by barcode
    # barcode:[filepath1,...filepathN]
    oldPathDictionary=oldPathDict(oldRoots)

    # Get dictionary of barcodes and their portal
    # portalDictionary[barcode]=portal
    portalDictionary=portalDict(occurrencesFile,portalName,colName)

    # Move files and keep track of files that were moved, and barcodes that don't have images 
    # barcodeNoImageDict[bcp]=portal
    # filesMovedDict[filename]=[barcode,portal,newpath]
    filesMovedDict,barcodeNoImageDict=moveFiles(newRoot,oldPathDictionary,portalDictionary,portalName)

    # Create dictionary barcode:[files moved]
    bcMovedDict={}
    for key in filesMovedDict:
        barcode=filesMovedDict[key][0]
        if barcode not in bcMovedDict:
            bcMovedDict[barcode]=[key]
        elif barcode in bcMovedDict:
            bcMovedDict[barcode]=[key]+bcMovedDict[barcode]


    # Get list of all new image paths
    newPathList = dictToBigList(filesMovedDict)

    # Get dictionary of images with issues. corruptImageDict[image name]=newimagepath
    corruptImageDict = corruptImageFinder(newPathList)

    # Output info in csv files
    # corruptImageDict[image name]= new image path
    # barcodeNoImageDict[bcp]=portal
    # filesMovedDict[filename]=[barcode,portal,newpath]

    dfBad = pd.DataFrame.from_dict(corruptImageDict,orient='index',columns=['File Path'])
    dfBad.index.name = 'Image File Name'
    dfBad.to_csv(os.path.join(outFolder,(portalName+"_corruptImages.csv")),sep=",")

    dfNoImage = pd.DataFrame.from_dict(barcodeNoImageDict,orient='index',columns=['Portal'])
    dfNoImage.index.name = 'Barcode'
    dfNoImage.to_csv(os.path.join(outFolder,(portalName+"_noImages.csv")),sep=",")

    # {filename:[barcode,portal,newpath]}
    dfFilesMoved = pd.DataFrame.from_dict(filesMovedDict,orient='index',columns=['Barcode','Portal','File Path'])
    dfFilesMoved.index.name = 'Image File Name'
    dfFilesMoved.to_csv(os.path.join(outFolder,(portalName+"_filesMoved.csv")),sep=",")

    # Number of barcodes in portal occurances.csv
    occurances=len(portalDictionary)
    # Number of barcodes moved
    bcMoved=len(bcMovedDict)
    # Number of barcodes with no image file
    noImage=len(barcodeNoImageDict)
    # If a != b + c raise error 
    amberAlert=occurances-(bcMoved+noImage)
    print('Moving files for '+str(portalName)+' portal')
    print('Portal barcodes: '+str(occurances))
    print('Relocated barcodes: '+str(bcMoved))
    print('No image barcodes: '+str(noImage))
    print('Unaccounted for barcodes: '+str(amberAlert))


if __name__=='__main__':
	# Set variables
    x = "ChatNoir"
    #x = "cbfla"
    #c = "imageStation"
    if x == "ChatNoir":
        ## Test on ChatNoir
        # Specify full path of current parent folder of images
        rootLSU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/'
        rootNO = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/no/'
        rootNLU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/nlu/'
        oldRoots = [rootLSU,rootNO,rootNLU]
        # Specify full path of the new parent folder for images
        newRoot='/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/'
        # Specify full path to folder for output lists
        outFolder='/Users/ChatNoir/Projects/HerbariumRA/'
        # Specify full path to DwC-A occurences.csv file downloaded from portal, name of portal, column name for barcodes in occurences.csv
        occurrencesFile="/Users/ChatNoir/Projects/HerbariumRA/Spreadsheets/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"
        portalName="bryophyte"
        colName="catalogNumber"

    elif x == "cbfla":
        ## Cyberflora
        # Specify full path of *current* parent folder of images
        rootLSU = '/home/gmount1/data_storage_fake/nfsshare/lsu/'
        rootNO = '/home/gmount1/data_storage_fake/nfsshare/no/'
        rootNLU = '/home/gmount1/data_storage_fake/nfsshare/nlu/'
        oldRoots = [rootLSU,rootNO,rootNLU]
        # Specify full path of the *new* parent folder for images
        newRoot='/home/gmount1/data_storage_fake/nfsshare/'
        # Specify full path to folder for output logs
        outFolder='/home/gmount1/'
        # Specify full path to DwC-A occurences.csv file downloaded from portal, name of portal, column name for barcodes in occurences.csv
        occurrencesFile="/home/gmount1/Database_Server/occurrencesfakecbfla.csv"
        portalName="vascular"
        colName="catalogNumber"

    elif x == "imageStation":
        ## Image Station
        # Specify full path of *current* parent folder of images
        rootLSU = '/mnt/c/Users/image/Desktop/gmount/output_fake/LSU/'
        oldRoots = [rootLSU]
        # Specify full path of the *new* parent folder for images
        newRoot='/mnt/c/Users/image/Desktop/gmount/output_fake/'
        # Specify full path to folder for output logs
        outFolder='/mnt/c/Users/image/Desktop/gmount/'
        # Specify full path to DwC-A occurences.csv file downloaded from portal, name of portal, column name for barcodes in occurences.csv
        occurrencesFile="/mnt/c/Users/image/Desktop/gmount/HerbariumRA/Database_Server/occurrencesfakeLaCie.csv"
        portalName="vascular"
        colName="catalogNumber"	

    else:
        print("Specify folders plz n thx")
    print(oldRoots,newRoot,outFolder,occurrencesFile,portalName,colName)
    main(oldRoots,newRoot,outFolder,occurrencesFile,portalName,colName)

