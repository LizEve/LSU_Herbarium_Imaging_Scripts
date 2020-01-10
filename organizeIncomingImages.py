import os
import itertools
#import pathlib2 as pathlib
import pathlib
import shutil 
import platform


def splitNumLet(b):
    '''
    Takes barcode in the format ABC_12345 and splits it into numbers and letters
    If barcode isnt in this format, it returns the original barcode
    '''
    try:
        b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
        return b_letters,b_numbers
    except ValueError:
        print("Incorrect barcode format. Excepting only one set of numbers and letters: "+str(b))
        return b

def creationDate(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    to transfer this into a human readable date - 
        import datetime 
        str(datetime.datetime.fromtimestamp(int(d)))
    """
    if platform.system() == 'Windows':
        # on windows ctime refers to creation date, NOT change time as on linux. 
        return os.path.getctime(path_to_file)
    else: # Likely on Linux, try to get birth time, default to mod time. 
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime  

def newPathName(sourceFolder,Filename,sourceFilePath,destinationPortalFolder,barcodeLength):
    '''
    Use old path to image, image file name, and destination parent folder (portal for LSU) to create a new path to move image. 
    Folder structure comes from barcode
    ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
    Improperly formated barcodes, or barcodes that are too long will have their destination be in the "BadBarcode" folder in the source folder for manual inspection and editing. 
    '''
    # Isolate barcode, remove anything that comes after . _ or -
    Barcode=Filename.split(".")[0].split("_")[0].split("-")[0]
    if len(Barcode) > barcodeLength:
        # File this into a "BadBarcode" folder for manual inspection and editing. 
        newDir = os.path.join(sourceFolder,"BadBarcode",Filename)
        newPath = os.path.join(sourceFolder,"BadBarcode")
    else: 
        # Split letters and numbers in two, returning two strings. LSU12345678 = LSU, 12345678. 
        # If barcode has the wrong format, the whole barcode will be returned. 
        splitBarcode=splitNumLet(Barcode)
        # If the barcode is returned as a single string
        if len(splitBarcode) == 1:
            # File this into a "BadBarcode" folder for manual inspection and editing. 
            newDir = os.path.join(sourceFolder,"BadBarcode",Filename)
            newPath = os.path.join(sourceFolder,"BadBarcode")
        # If the barcode was split into two strings, continue to split and create new file path
        elif len(splitBarcode) == 2:
            Collection,number=splitBarcode
            # Split apart number to create new file path
            lastThree=number[-3:] # this isnt nessecary, just to double check things
            cutoffThree=number[:-3]
            secondFolder=cutoffThree[-3:]
            firstFolder=cutoffThree[:-3]
            # Create folders from barcode and portal information
            # ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
            newPath=os.path.join(destinationPortalFolder,Collection,firstFolder,secondFolder,fileName.upper())
            # Get directory path to check if folders need to be created
            newDir=os.path.dirname(newPath)
    return newDir,newPath

def moveFiles(sourceFolder,destinationFolder,portalFolders,otherFolders,barcodeLength,outLogsuffix):


    # Iterate through list of user defined organizing source folders, for LSU these are portal names 
    for folder in portalFolders:
        # Get full folder path 
        folderPath=os.path.join(sourceFolder,folder)
        # Iterate through files in folder 
        for filename in os.listdir(folderPath):
            # Change file names to uppercase for consistancy later on
            FileName=filename.upper()
            # Get full path for file 
            sourceFilePath=os.path.join(folderPath,filename)
            # Get creation date for file, or last modification date if creation date cannot be recovered
            birthDate=creationDate(sourceFilePath)
            # For those files to be sorted as normal set destination path
            if folder not in otherFolders:
                # Path to portal folder 
                destinationPortalFolder = os.path.join(destinationFolder,folder)
                # Create path to destination file and parent folder 
                # This will also check for barcode format and length, sending all bad barcodes to a seperate folder for manual inspection.
                destinationFolderPath,destinationFilePath = newPathName(sourceFolder,Filename,sourceFilePath,destinationPortalFolder,barcodeLength)
            # For those files who are moved as is in their folders, set destination path
            elif folder in otherFolders:
                # Get any nested folders that exists beyond the organizing folder, for LSU it will be named "Random"
                # Strip the source folder path, keeping any other nested folder structure within "Random"
                nestedFolderPath=sourceFilePath.strip(folderPath)
                # Create destination file path 
                destinationFilePath=os.path.join(destinationFolder,nestedFolderPath)
            # Try to move file 
            try:
                shutil.move(sourceFilePath,destinationFilePath)
                # Get day that the file was created or modified(Ex 2019-06-07) and add customized suffix and file extension
                logFileName=str(datetime.datetime.fromtimestamp(int(birthDate))).split()[0]+outLogsuffix
                # Create path to log file 
                logFilePath=os.path.join(sourceFolder,"Logs",logFileName)
                # Open log file and write down destination path
                writeLog = open(logFilePath,'a')
                writeLog.write(destinationFilePath)
                writeLog.close()
            except FileNotFoundError:
                pass

def main():
    # All of the following folders should already exist. 
    # As well as a folder named "BadBarcode" and one named "Logs" in your destination folder 
    # Make sure paths have a trailing forward slash at the end '/'. otherwise everything will fail. 

    # Folder of images on computer
    
    sourceFolder='/mnt/c/Users/Image/Desktop/Imaging/'
    
    # Folder for long term storage 
    
    destinationFolder='/mnt/e/CFLA-LSU-Station2/LSUCollections/'
        
    # The following folders should exist in both the source and destination folder 
    
    # List of folders that correspond to how you want to store your images
    # For LSU images are stored based on the portal they will be uploaded to online.
    
    portalFolders=['Algae','Bryophyte','Fungi','Lichen','Vascular']
    
    # Extra folders for one time projects. Barcodes will not be checked, and any nested folders will be moved as is. 
    
    otherFolders=['Random']
    
    # Maximum length for legitimate barcode, does not count anything trailing an underscore "_"
    
    barcodeLength=15
    
    # String that will be appended to all out logs. Can customize for computer. 
    # Make sure this is different from the string appended to your server logs. 
    # Add whatever file extension you want. ".txt" is reccomended so simple text editors can open the files.
    outLogsuffix="_workstation1.txt"
    
    newPaths,badbarcode,duplicate=moveFiles(sourceFolder,destinationFolder,portalFolders,otherFolders,barcodeLength,outLogsuffix)

    '''
    Extra notes 
    *File name restrictions*
    File names are expected to start with a barcode. This barcode should start with letters followed by ONLY numbers.
    Folders will be created first using the letters, then using the numbers. 
    Extra notes or tags, such as numbering multiple files should come after an underscore "_"
    Ex: LSU01234567.JPG or LSU01234567_1.JPG
    All file names will be changed to all caps if they are not already. Except those files in the other/random folders
    '''

if __name__ == "__main__":
    main()
