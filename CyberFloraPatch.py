import os
import fnmatch
import re
import glob
import shutil
import datetime

def findfiles(which, where='.'):
    '''Returns list of filenames from `where` path matched by 'which'
       shell pattern. Matching is case-insensitive.'''
    # https://gist.github.com/techtonik/5694830
    rule = re.compile(fnmatch.translate(which), re.IGNORECASE)
    return [name for name in os.listdir(where) if rule.match(name)]

def barcode2List(b):
    '''
    Takes a single barcode and returns a list of numbers
    Only takes NO or LSU barcodes in the following format, if a different format, files will not be moved or listed
    LSU00010203 -> ['00','01','02','03']
    NO0010203 -> ['0','01','02','03']
    '''
    if b[0:2] == "LS":
        # Grab only the numbers of the barcode
        barcode = re.sub('[^0-9]','', b)
        # Split string every 2 characters (stackxchange - "split string every nth character?")
        barcodeList = re.findall('.{1,2}', barcode)
        return barcodeList
    
    elif b[0:2] == "NO":
        # Grab only the barcode
        barcode = re.sub('[^0-9]','', b)
        # Save first number from barcode as a list
        firstList = [barcode[0]]
        # Save the rest of barcode
        sixDigitsNO = barcode[1:]
        # Create list from rest of barcode, paste to first digit
        sixDList = re.findall('.{1,2}', sixDigitsNO)
        barcodeList = firstList + sixDList
        return barcodeList
    else:
        print("Non LSU or NO barcode detected. This file will NOT be moved or listed: "+str(b))
    
def bcList2folders(bcList,root_path):
    '''
    Takes barcode list of digits
    Creates & traverses nested folders 
    Returns path of barcode 
    '''
    curDir = root_path
    for i in bcList:
        # Remove leading 0 for single digit numbers
        folder=str(int(i))
        newDir = os.path.join(curDir,folder)
        if os.path.isdir(newDir):
            curDir=newDir
        else:
            os.makedirs(newDir)
            curDir=newDir
    return curDir
    
def moveFiles(bcL,root_path,incomingFolder):
    '''
    Takes barcode list of digits, and root path for specific collection
    Moves files into final resting place
    Returns barcode, path of barcode, and all files moved for that barcode
    '''
    # Use barcode list to traverse/make folders, get final path for barcode
    folderPath=bcList2folders(bcL,root_path)
    
    # Turn barcode list back into barcode string
    barCode=''.join(bcL)
    # List all files matching barcode
    allFiles=(glob.glob(os.path.join(incomingFolder,'*'+barCode+'*')))
    
    # Move all files into their final resting place
    for oneFile in allFiles:
        movedFilePath=os.path.join(folderPath, os.path.basename(oneFile))
        shutil.move(oneFile,movedFilePath)
    return barCode,folderPath,allFiles

def moveIncomingFiles(uniqueBarCodes,incomingFileList,incomingFolder,lsuFolder,noFolder):
    '''
    Takes list of unique barcodes and list of files to be moves
    Calls on other scripts to transform barcodes into paths, make folders when needed, and then move files into appropriate folders
    Returns lists of which files were moves and the paths they were moved to
    '''
    # Barcode strings into barcode lists, all numbers preserved
    barcodeLists = []
    for ub in uniqueBarCodes:
        barcodeLists.append(barcode2List(ub))

    # Make/traverse folders for each barcode and move files
    folderPathList=[]
    movedFileList=[]
    movedBarcodeList=[]
    for bcL in barcodeLists:
        # Sort based on first set of digits into lsu and no(tulane) barcodes
        if str(bcL[0]) == str("00"):
            root_path=lsuFolder
            x = moveFiles(bcL,root_path,incomingFolder)
        elif str(bcL[0]) == str("0"):
            root_path=noFolder
            x = moveFiles(bcL,root_path,incomingFolder)
        else:
            print("Barcode does not start with 0. There is probably an error. Has not been filed or listed: "+str(bcL))
            
        # Keep lists of: files moved to folders, paths to folders, barcodes
        for z in x[2]:
            movedFileList.append(os.path.basename(z))
        folderPathList.append(x[1])
        movedBarcodeList.append(x[0])
    return folderPathList,movedBarcodeList,movedFileList
        
def main():      
    # Local testing
    incomingFolder = "/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/cfla/incoming"
    outFileFolder = "/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/cfla/incoming_records2018"
    lsuFolder="/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/"
    noFolder="/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/no/vasc_plants/"

    #### Set folder paths and output log files ######
    #incomingFolder = "/home/silverimageftp/incoming/"
    #outFileFolder = "/data_storage/nfsshare/incoming_logs_2018"
    #lsuFolder="/data_storage/nfsshare/lsu/"
    #noFolder="/data_storage/nfsshare/no/vasc_plants/"
    # Make file name based on date
    outFileName=str(datetime.date.today()).replace("-","_")+str("_movedimages.out")
    outFilePath=os.path.join(outFileFolder,outFileName)


    ##### Working with incoming files ###### 

    # Count number of files in incoming folder before moving 
    fileBefore = next(os.walk(incomingFolder))[2] 

    # List of all jpg files in incoming folder
    incomingFileList=findfiles("*jpg",incomingFolder)

    # Get set of unique barcodes
    uniqueBarCodes=set()
    for f in incomingFileList:
        # Strip _ from files
        b=re.split("_|\.",f)[0]
        uniqueBarCodes.add(b)

    # Make folders and move files, returns lists of what was moved and where
    folderPathList,movedBarcodeList,movedFileList=moveIncomingFiles(uniqueBarCodes,incomingFileList,incomingFolder,lsuFolder,noFolder)  

    # Count number of files in incoming folder after moving 
    fileAfter= next(os.walk(incomingFolder))[2]

    ##### Write info to file ##### 
    
    # Open file, then write a bunch of stuff. 
    outFile = open('%s' % outFilePath, 'wa')
    outFile.write("Date Time\n")
    outFile.write([str(datetime.datetime.now())][0]+"\n"+"\n")
    outFile.write("Number of files moved\n")
    outFile.write("Barcodes | Total Files\n")
    outFile.write(str(len(movedBarcodeList))+"  |  "+str(len(movedFileList))+"\n"+"\n")
    outFile.write("Number of files left in incoming folder: "+str(len(fileAfter))+"\n"+"\n")
    if len(fileAfter) != 0:
        outFile.write("PLEASE MOVE THESE MANUALLY\n")
        for i in fileAfter:
            outFile.write("%s\n" % i)
        outFile.write("\n")
    outFile.write("Files Moved:\n\n")
    for p in movedFileList:
        outFile.write("%s\n" % p)
    outFile.close
    outFile.flush()
    

if __name__=='__main__':
    # Adding some for standard output, shouldn't need this, but somewhere to write errors to just in case. 
    print("JOB STARTED - "+str(datetime.datetime.now()))
    main()
    print("JOB FINISHED - "+str(datetime.datetime.now()))