import os
import csv
from csv import DictReader
import itertools
import pathlib2 as pathlib
import shutil
from PIL import Image
import pandas as pd
import pickle

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
        #barcode=fileName.split(".")[0].split("_")[0].split("-")[0]
        #print barcode
        # if barcode isnt in the dictionary, add it with file, if it is, add any extra files. 
        if barcode not in oldPathDictionary:
            oldPathDictionary[barcode]=[oldPath]
        elif barcode in oldPathDictionary:
            oldPathDictionary[barcode]=[oldPath]+oldPathDictionary[barcode]
        else:
            print("This should never happen")
    output = open("oldPathDictionaryMay30.pkl",'wb')
    pickle.dump(oldPathDictionary,output)
    output.close()
    return oldPathDictionary

def portalDict(occurrencesFile,portalName,colName="catalogNumber"):
    '''
    Get dictionary of all barcodes and respective portal names
    Input - occurrences.csv, name of portal, and name of column with barcodes
    Output - Dictionary of barcodes and portal name for each barcode
    '''
    csv_file = open(occurrencesFile, "rU")
    catNumList = [row[colName] for row in DictReader(csv_file)]
    csv_file = open(occurrencesFile, "rU")
    portalNameList = [row[portalName] for row in DictReader(csv_file)]
    csv_file.close()
    portalDictionary={}
    l=len(catNumList)
    for n in range(0,l):
        portalDictionary[catNumList[n]]=portalNameList[n]
    # return an all caps dicts
    output = open("portalDictionaryMay30.pkl",'wb')
    pickle.dump(portalDictionary,output)
    output.close()
    return portalDictionary

def compareFiles(oldPathDictionary,portalDictionary):
    '''
    Compare files based on barcode
    Input - Dictionary of old paths. Dictionary of barcodes and their portal
    Output - Dictionary of files in common {filename:[barcode,portal,newpath]}. 
    Dictionary of barcodes with no image {barcode:portal}
    '''
    # Make all keys(barcodes) into uppercase. values(list of paths) will stay as is. 
    oldDictionary_BCcaps = dict((k.upper(), v) for k, v in oldPathDictionary.items())
    portalDictionary_BCcaps = dict((k.upper(), v) for k, v in portalDictionary.items())
    # filename:[barcode,portal,newpath]
    barcodeImageDict={}
    # barcode:portal
    barcodeNoImageDict={}
    imageNoBarcodeDict={}
    imageOut = open("barcodeImageDictMay30.txt",'w')
    noimageOut = open("barcodeNoImageDictMay30.txt",'w')
    print(len(oldDictionary_BCcaps),len(portalDictionary_BCcaps))
    # Iterate through barcodes that are in the portal database
    for bcp in portalDictionary_BCcaps:
        # If barcode has image files... 
        if bcp in oldDictionary_BCcaps:
            barcodeImageDict[bcp]=portalDictionary_BCcaps[bcp]
            imageOut.write(bcp+":"+barcodeImageDict[bcp]+"\n")
        # If barcode has no image files
        elif bcp not in oldDictionary_BCcaps:
            # keep track of specify records with no image file. barcode:portal
            barcodeNoImageDict[bcp]=portalDictionary_BCcaps[bcp]
            noimageOut.write(bcp+":"+barcodeNoImageDict[bcp]+"\n")
    imageOut.close()
    noimageOut.close()
    print("done comparing")
    #bID = open("barcodeImageDict.pkl",'wb')
    #pickle.dump(barcodeImageDict,bID)
    #bID.close()
    #bnID = open("barcodeNoImageDict.pkl",'wb')
    #pickle.dump(barcodeNoImageDict,bnID)
    #bnID.close()
    #print("saved pickle dictionary comparisons")
    return barcodeImageDict,barcodeNoImageDict

def dictToBigList(filesMovedDict):
    '''
    Turns dictionary of filename:[barcode,portal,newpath] into continuous list of all newpaths
    '''
    # Make one single list of all image files
    print("making list from dictionary")
    allFilesList=[]
    for paths in filesMovedDict.values():
        allFilesList.append(paths[0])
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
                    print(str(e)+f)
        # If image doesnt open as an image, take note
        except IOError as i:
                corruptImageDict[os.path.basename(f)]=f
                #notImageDict[os.path.basename(f)]=f
                print(str(i)+f)
    return corruptImageDict

# Specify full path to folder for output lists
#outFolder='/Users/ChatNoir/Projects/HerbariumRA/'
#outFolder='/mnt/c/Users/image/Desktop/gmount/'
outFolder='/home/gmount1/'

# Specify full path to DwC-A occurences.csv file downloaded from portal, name of portal, column name for barcodes in occurences.csv
occurrencesFile="/home/gmount1/masterDF_may27.csv"
portalName="portalName"
colName="catalogNumber"


# Specify full path of current parent folder of images
rootLSU = '/data_storage/nfsshare/lsu/'
rootNO1 = '/data_storage/nfsshare/no/vas_plants/'
rootNO2 = '/data_storage/nfsshare/no/0/'
rootNLU = '/data_storage/nfsshare/nlu/'
rootLSUS = '/data_storage/nfsshare/lsus/'
oldRoots = [rootLSU,rootNO1,rootNO2,rootNLU,rootLSUS]

# Get dictionary of current image paths, organized by barcode
# barcode:[filepath1,...filepathN]
oldPathDictionary=oldPathDict(oldRoots)
print("Got image path dictionary")
# Get dictionary of barcodes and their portal
# portalDictionary[barcode]=portal
portalDictionary=portalDict(occurrencesFile,portalName,colName)
print("Got portal dictionary")

# Compare and keep track of barcodes that have images, and barcodes that don't have images 
# barcodeNoImageDict[bcp]=portal
barcodeImageDict,barcodeNoImageDict=compareFiles(oldPathDictionary,portalDictionary)


# Get list of all new image paths
allFilesList = dictToBigList(oldPathDictionary)

# Get dictionary of images with issues. corruptImageDict[image name]=newimagepath
#corruptImageDict = corruptImageFinder(allFilesList)

# Output info in csv files
# corruptImageDict[image name]= new image path
# barcodeNoImageDict[bcp]=portal
# filesMovedDict[filename]=[barcode,portal,newpath]

#dfBad = pd.DataFrame.from_dict(corruptImageDict,orient='index',columns=['File Path'])
#dfBad.index.name = 'Image File Name'
#dfBad.to_csv(os.path.join(outFolder,(portalName+"_corruptImages.csv")),sep=",")

#dfNoImage = pd.DataFrame.from_dict(barcodeNoImageDict,orient='index',columns=['Portal'])
#dfNoImage.index.name = 'Barcode'
#dfNoImage.to_csv(os.path.join(outFolder,(portalName+"_noImages.csv")),sep=",")
#
## {filename:[barcode,portal,newpath]}
#dfFilesMoved = pd.DataFrame.from_dict(barcodeImageDict,orient='index',columns=['Barcode','Portal','File Path'])
#dfFilesMoved.index.name = 'Image File Name'
#dfFilesMoved.to_csv(os.path.join(outFolder,(portalName+"_hasImages.csv")),sep=",")
#


## Number of barcodes in portal occurances.csv
#occurances=len(portalDictionary)
## Number of barcodes with image
#hasImage=len(barcodeImageDict)
## Number of barcodes with no image file
#noImage=len(barcodeNoImageDict)
## If a != b + c raise error 
#amberAlert=occurances-(bcMoved+noImage)
#print('Portal barcodes: '+str(occurances))
#print('Has image barcodes: '+str(hasImage))
#print('No image barcodes: '+str(noImage))
#print('Unaccounted for barcodes: '+str(amberAlert))

