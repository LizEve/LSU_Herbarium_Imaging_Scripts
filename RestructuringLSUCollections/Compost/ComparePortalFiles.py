import os
import csv
from csv import DictReader
import itertools
import pathlib2 as pathlib
import shutil
from PIL import Image
import pandas as pd
import pickle 


def save_obj(obj, fname, mainDir):
    # saves binary python object in "obj" folder in main directory 
    dirPath = os.path.join(mainDir,"obj")
    fPath = os.path.join(dirPath,fname+".pkl")
    if not os.path.exists(dirPath):
		os.mkdir(dirPath)	
    with open(fPath, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(fname, mainDir):
    # Reads binary python object 
    fPath = os.path.join(dirPath,"obj",fname+".pkl")
    with open('obj/' + fname + '.pkl', 'rb') as f:
        return pickle.load(f)


def oldPathDict(roots):
    '''
    Get dictionary of all image files in root folders 
    Input- list of root directorys
    Output- dictionary of barcode: [list of absolute paths to all files with barcode]
    Details- does not see any txt, _l, _m, _s, files. Does not specify file extension
    <https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files>
    '''
    oldPathList=[]
    oldPathDictionary={}
    unwanted=["_m","_s","txt","_l"]
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
            oldPathDictionary[barcode.upper()]=[oldPath]
        elif barcode in oldPathDictionary:
            oldPathDictionary[barcode.upper()]=[oldPath]+oldPathDictionary[barcode]
        else:
            print("This should never happen")
    return oldPathDictionary

def portalDict(portalFiles,outFolder,colName="catalogNumber",appendDict=["F",""]):
    '''
    Get dictionary of all barcodes and respective portal names
    Input - Dictionary of portalname:pathtocsvfile, folder for output files, and name of column with barcodes, if you want to append to previous dict 
    Output - Dictionary of barcodes and portal name for each barcode
    '''
    if appendDict[0] == "T":
        portalDictionary=load_obj(appendDict[1],outFolder)
    else:
        portalDictionary={}
    doublePortal={}
    for portalName in portalFiles:  
        occurrenceFile=portalFiles[portalName]
        with open(occurrenceFile, "r",encoding="utf8", errors='ignore') as csv_file:
            catNumList = [row[colName] for row in DictReader(csv_file)]
        for n in catNumList:
            if n.upper() not in portalDictionary:
                portalDictionary[n.upper()]=portalName
            if n.upper() in portalDictionary:
                doublePortal[n.upper()]=str(portalName+","+portalDictionary[n.upper()])
    # Record any barcodes that show up in multiple portals 
    df = pd.DataFrame.from_dict(doublePortal,orient='index',columns=['Portals'])
    df.index.name = 'Barcode'
    df.to_csv(os.path.join(outFolder,("barcodeMultPortals.csv")),sep=",")
    # return an all caps dicts
    return portalDictionary

def compareFiles(oldPathDictionary,portalDictionary):
    '''
    Organizes files based on barcode and portal. 
    Input - New parent folder. Dictionary of old paths. Dictionary of barcodes and their portal
    Output - Dictionary of files moved {filename:[barcode,portal,newpath]}. 
    Dictionary of barcodes with no image {barcode:portal}
    '''
    # barcode:portal
    recordNoImageDict={}
    imageNoRecordDict={}
    recordNoImageList=[]
    imageNoRecordList=[]
    # Iterate through barcodes that are in the portal database
    for bc in portalDictionary:
        # If barcode has no image files
        if bc not in oldPathDictionary:
            # keep track of specify records with no image file. barcode:portal
            recordNoImageDict[bc]=portalDictionary[bc]
            recordNoImageList.append(bc)
    for bc in oldPathDictionary:
        if bc not in portalDictionary:
            imageNoRecordDict[bc]="norecord"
            imageNoRecordList.append(bc)
    return recordNoImageDict,imageNoRecordDict


outFolder='/Users/ChatNoir/Projects/HerbariumRA/'

# Specify full path of current parent folder of images
rootLSU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/'
rootNO = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/no/'
rootNLU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/nlu/'
roots = [rootLSU,rootNO,rootNLU]                    
  
# Get dictionary of current image paths, organized by barcode
# barcode:[filepath1,...filepathN]
oldPathDictionary=oldPathDict(roots)


# Specify full path to DwC-A occurences.csv file downloaded from portal, name of portal, column name for barcodes in occurences.csv
vascularSheet="/Users/ChatNoir/Projects/HerbariumRA/Spreadsheets/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"
bryophyteSheet="/Users/ChatNoir/Projects/HerbariumRA/Spreadsheets/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"
fungiSheet="/Users/ChatNoir/Projects/HerbariumRA/Spreadsheets/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"
algeaSheet="/Users/ChatNoir/Projects/HerbariumRA/Spreadsheets/LSU-Bryophytes_backup_2018-10-01_115050_DwC-A/occurrencesfake.csv"


portalFiles={"vascular":vascularSheet,"bryophyte":bryophyteSheet,"fungi":fungiSheet,"algea":algeaSheet}
colName="catalogNumber"

# Get dictionary of barcodes and their portal
# portalDictionary[barcode]=portal
portalDictionary=portalDict(portalFiles,outFolder,colName)

# Write dictionary to binary file 
# Can add to this file 

# Move files and keep track of records that don't have images, and images that don't have records
recordNoImageDict,imageNoRecordDict=compareFiles(oldPathDictionary,portalDictionary)


dfRNI = pd.DataFrame.from_dict(recordNoImageDict,orient='index',columns=['Portal'])
dfRNI.index.name = 'Barcode'
dfRNI.to_csv(os.path.join(outFolder,("recordNoImage.csv")),sep=",")
                
            
            
dfINR = pd.DataFrame.from_dict(imageNoRecordDict,orient='index',columns=['Portal'])
dfINR.index.name = 'Barcode'
dfINR.to_csv(os.path.join(outFolder,("imageNoRecord.csv")),sep=",")
                

