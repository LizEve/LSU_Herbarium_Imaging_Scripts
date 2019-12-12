import os
import itertools
import pickle
import platform
import csv
import re 
import pathlib2 as pathlib
import shutil 


def fileNametoPath(newName,newPortal,newRoot):
    '''
    Use new name and portal, spits out new path
    requires splitNumLet function
    '''
    # get just file name without extension 
    newerName = newName.split('.')[0]
    # get collection letters 
    collection = re.split('(\d+)',newerName)[0]
    # get file numbers 
    number = newerName.strip(collection)
    # Split apart barcode number to create new file path
    lastThree=number[-3:] # this isnt nessecary, just to double check things
    cutoffThree=number[:-3]
    secondFolder=cutoffThree[-3:]
    firstFolder=cutoffThree[:-3]
    # Create folders from barcode and portal information
    # ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
    newPath=os.path.join(newRoot,newPortal,collection,firstFolder,secondFolder,newName.upper())
    # Get path to directory only, to make a new one later if needed 
    newDir=os.path.dirname(newPath)
    return newDir,newPath

def moveFiles(roots,moveList,newRoot):
    '''
    Get dictionary of all image files in root folders 
    Input- root directory, csv file with "oldName	newName	oldPortal	newPortal"
    '''

    # keeping dictionary of stuff just in case i need it? Name is random. 
    rosemary = {} # rosemary[oldName]=[newName,oldPortal,newPortal]

    # List of files that already exist in the correct place 
    jenniesList = []

    # Open CSV file by line 
    with open(moveList) as f:
        # skip header 
        next(f)
        for line in f:
            # split into bits and add to dictionary. 
            # ['NO0074995.CR2,NO0074995.CR2,NoPortal,Vascular']
            csvRow = line.split(',')
            oldName = csvRow[0]
            newName = csvRow[1]
            oldPortal = csvRow[2]
            newPortal = csvRow[3].strip('\n')

            # add to dictionary, not sure if I will need this. 
            rosemary[oldName]=[newName,oldPortal,newPortal]
            
            # Collection 
            oldCollection = re.split('(\d+)',oldName)[0]
            # need to get collection for old file. 
            oldPath = os.path.join(newRoot,oldPortal,oldCollection,oldName)
            oldPathCR2 = os.path.splitext(oldPath)[0]

            # check if old file exists
            if os.path.exists(oldPathCR2):
                # check if old file is to be moved or deleted 
                if newPortal == 'x' or newName == 'delete':
                    # delete file 
                    os.remove(oldPath)
                    os.remove(oldPathCR2)
                    print("Deleting "+str(oldPath))
                else:
                    # get new portal path 
                    newDir,newPath = fileNametoPath(newName,newPortal,newRoot)
                    newPathCR2 = os.path.splitext(newPath)[0]
                    # If newPath to file does not exist already 
                    if not os.path.exists(newPathCR2):
                        # check if folder for new file needs to be created 
                        if not os.path.exists(newDir):
                            pathlib.Path(newDir).mkdir(parents=True, exist_ok=True) 

                        # Move file
                        print("Moving "+str(oldPath)+" to "+str(newPath))
                        shutil.move(oldPath,newPath)
                        shutil.move(oldPathCR2,newPathCR2)

                    else: # if it already exists, save in list for jennie. 
                        jenniesList.append(newName)
                        print(str(newPath)+" already exists!")
            else:
                print("File path bad "+str(oldPath))
    return jenniesList


def main():
    # Full path to folder for output lists
    outFolder='/home/ggmount/'
    roots = ['/mnt/LSUCollections/BadBarcode', '/mnt/LSUCollections/NoPortal']
    newRoot = '/mnt/LSUCollections/'
    moveList = '/home/ggmount/BadBarcodeNoPortal_Nov25.csv'
    # Move files
    jList = moveFiles(roots,moveList,newRoot)
    # write jlist to file
    with open('Duplicates_Dec.csv', 'a') as f:
        writer = csv.writer(f)
        for val in jList:
            writer.writerow([val])
    
    # Full path to folder for output lists
    roots = ['/mnt/LSUCollectionsWS1/LSUCollections/BadBarcode', '/mnt/LSUCollectionsWS1/LSUCollections/NoPortal']
    newRoot = '/mnt/LSUCollectionsWS1/LSUCollections/'
    moveList = '/home/ggmount/BadBarcodeNoPortal_Nov25.csv'
    # Move files
    jList = moveFiles(roots,moveList,newRoot)
    # write jlist to file
    with open('Duplicates_Dec.csv', 'a') as f:
        writer = csv.writer(f)
        for val in jList:
            writer.writerow([val])

if __name__ == "__main__":
    main()