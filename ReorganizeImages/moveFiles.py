import pickle 
import os
import itertools
import pathlib2 as pathlib
import shutil 
import platform

def pickleOpen(p):
    file=open(p,'rb')
    data = pickle.load(file)
    file.close()
    return data


def splitNumLet(b):
    # Split apart letters and numbers from barcode
    try:
        b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
        return b_letters,b_numbers
    except ValueError:
        print("Incorrect barcode format. Excepting only one set of numbers and letters: "+str(b))
    
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    to transfer this into a human readable date - 
        import datetime 
        str(datetime.datetime.fromtimestamp(stat.st_mtime))
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def newPathNames(b,p,new_root,portal):
    '''
    Use old path to image, and portal to create a new path to place images. 
    '''
    # Grab name of file, collection (lsu,no,etc), numerical part of barcode, portal
    fileName=p.split("/")[-1]
    collection,number=splitNumLet(b)
    # Split apart barcode number to create new file path
    lastThree=number[-3:] # this isnt nessecary, just to double check things
    cutoffThree=number[:-3]
    secondFolder=cutoffThree[-3:]
    firstFolder=cutoffThree[:-3]
    # Create folders from barcode and portal information
    # ex: LSU01020304 -> root/portal/lsu/01/020/LSU01020304.jpg 
    newPath=os.path.join(new_root,portal,collection,firstFolder,secondFolder,fileName.upper())
    # Get directory path to check if folders need to be created
    newDir=os.path.dirname(newPath)
    return newDir,newPath,fileName.upper()

def pklDictOut(outDict,outPath,outFileName):
    # Output dictionaries into pkl files 
    outFile = open(os.path.join(outPath,outFileName+".pkl"),'wb')
    pickle.dump(outDict,outFile)
    outFile.close()

def addLarge(barcode,oldPath,newPath,nolarge_dict):
    # Assume paths to old "large" file (which is smaller) for image file
    # Using a few options for case. 
    lp=str(pathlib.Path(oldPath).with_suffix(""))+str("_L.JPG")
    lp1=str(pathlib.Path(oldPath).with_suffix(""))+str("_l.JPG")
    lp2=str(pathlib.Path(oldPath).with_suffix(""))+str("_L.jpg")
    lp3=str(pathlib.Path(oldPath).with_suffix(""))+str("_l.jpg")
    # All new files are uppercase. fight me about it. 
    lnewPath=str(pathlib.Path(newPath).with_suffix(""))+str("_L.JPG")
    # Try to copy large file to new location. If no large exists, add to dict of files that need larges
    try:
        shutil.copy2(lp,lnewPath)
    except FileNotFoundError:
        try:
            shutil.copy2(lp1,lnewPath)
        except FileNotFoundError:
            try:
                shutil.copy2(lp2,lnewPath)
            except FileNotFoundError:
                try:
                    shutil.copy2(lp3,lnewPath)
                except FileNotFoundError:
                    nolarge_dict[barcode]=newPath
    return nolarge_dict


def moveFiles(new_root,barcode_dict,portal_dict,unwanted,noPortalPath,badBarcodePath,rerun):

    # Make all barcodes into caps for comparison
    barcode_Dict=dict((k.upper(), v) for k, v in barcode_dict.items())
    portal_Dict=dict((k.upper(), v) for k, v in portal_dict.items())

    # Start dictionary to put new file paths in
    # filename: [barcode, portal, date, current(new) path]
    new_dict={}
    nolarge_dict={}
    badbarcode_dict={}
    duplicate_dict={}

    # Iterate through every barcode in image barcode dict
    for b in barcode_Dict:

        # Split apart letters and numbers from barcode
        try:
            b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]

        # For bad barcodes move them to a special folder for Jennie to check. 
        except ValueError:

            # Iterate through all file paths in bad barcode dict
            for p in barcode_Dict[b]:

                # Ignore files in "unwanted" list 
                if any(x in p for x in unwanted):
                    pass

                else:
                    # Make new path to folder for images that have a bad barcode 
                    fName=os.path.basename(p)
                    newPath=os.path.join(badBarcodePath,fName.upper())

                    # Copy file, preserving permissions 
                    shutil.copy2(p,newPath)
                
                    # Get creation date 
                    d = creation_date(p)

                    #filename: [barcode,  date, old path]
                    badbarcode_dict[fileName]=[b,d,p]
                    print("Incorrect barcode format. Putting files from ,"+str(b)+", into "+str(badBarcodePath))
        
        # For all good barcodes that can be split into Letters/Numbers
        # If barcode is found in records, move it into correct portal file
        if b in portal_Dict:

            # Get portal for barcode 
            portal=portal_Dict[b]

            # Iterate through all file paths in barcode dict
            for p in barcode_Dict[b]:

                # Ignore files in "unwanted" list 
                if any(x in p for x in unwanted):
                    pass

                else:
                    # Get new file path and uppercase file name 
                    newDir,newPath,fileName=newPathNames(b,p,new_root,portal)

                    # Check if file exists at new path
                    if not os.path.exists(newPath):

                        # Make new directories if needed https://docs.python.org/3/library/pathlib.html
                        if not os.path.exists(newDir):
                            pathlib.Path(newDir).mkdir(parents=True, exist_ok=True) 

                        # Copy file, preserving permissions 
                        shutil.copy2(p,newPath)

                        # Try and copy large file if it exists, if not, add to list. 
                        nolarge_dict = addLarge(b,p,newPath,nolarge_dict)
                    
                        # Get creation date 
                        d = creation_date(p)

                        #filename: [barcode, portal, date, current(new) path]
                        new_dict[fileName]=[b,portal,d,newPath]
                    # If path exists, check if this is a rerun, if not, put newest file in folder. make note of duplicates
                    elif os.path.exists(newPath):
                        # Get creation dates for file already moved, and the one that is similar to it. likely different due to case sensitive issues.  
                        d = creation_date(p)
                        d1 = creation_date(newPath)
                        # If dates are the same, probably rerunning script, dont add to duplicate dict
                        if d == d1:
                            pass
                        else:
                            # Add to duplicate dict 
                            duplicate_dict[b]=barcode_dict[b]
                        # If this file is newer, replace older file. Rerun or not we want to move newer file to main folder.
                        if d > d1:
                            # Copy file, preserving permissions 
                            shutil.copy2(p,newPath)

                            # Try and copy large file if it exists, if not, add to list. 
                            nolarge_dict = addLarge(b,p,newPath,nolarge_dict)

                            #filename: [barcode, portal, date, current(new) path]
                            new_dict[fileName]=[b,portal,d,newPath]

        # If no record in master list. Move to special folder. 
        # Also try and move large file. Add to list of moved files.             
        elif b not in portal_Dict:
            # Iterate through all file paths in barcode dict
            for p in barcode_Dict[b]:

                # Ignore files in "unwanted" list 
                if any(x in p for x in unwanted):
                    pass
                else:
                    # Make new path to folder for images that don't have barcode in master list. 
                    fName=os.path.basename(p)
                    newPath=os.path.join(noPortalPath,fName.upper())

                    # Check if file exists at new path
                    if not os.path.exists(newPath):
                        # Copy file, preserving permissions 
                        shutil.copy2(p,newPath)

                        # Try and copy large file if it exists, if not, add to list. 
                        nolarge_dict = addLarge(b,p,newPath,nolarge_dict)
                    
                        # Get creation date 
                        d = creation_date(p)

                        #filename: [barcode, portal, date, current(new) path]
                        new_dict[fileName]=[b,"NoPortal",d,newPath]

                    # If path exists, check if this is a rerun, if not, put newest file in folder. make note of duplicates
                    elif os.path.exists(newPath):
                        # Get creation dates for file already moved, and the one that is similar to it. likely different due to case sensitive issues.  
                        d = creation_date(p)
                        d1 = creation_date(newPath)
                        # If dates are the same, probably rerunning script, dont add to duplicate dict
                        if d == d1:
                            pass
                        else:
                            # Add to duplicate dict 
                            duplicate_dict[b]=barcode_dict[b]
                        # If this file is newer, replace older file. Rerun or not we want to move newer file to main folder.
                        if d > d1:
                            # Copy file, preserving permissions 
                            shutil.copy2(p,newPath)

                            # Try and copy large file if it exists, if not, add to list. 
                            nolarge_dict = addLarge(b,p,newPath,nolarge_dict)

                            #filename: [barcode, portal, date, current(new) path]
                            new_dict[fileName]=[b,"NoPortal",d,newPath]

                    print("No record for "+str(b)+" moved to "+str(noPortalPath))

    return new_dict,nolarge_dict,badbarcode_dict,duplicate_dict


def main():
    # Read in dictionaries 
    # dict1 - filename: [barcode, date, current path]
    # dict2 - barcode: [list of absolute paths to all files with barcode]
    # portal - barcode: portal
    barcode_pkl='/home/ggmount/lsu_imageFiles_Aug09_barcode.pkl'
    portal_pkl='/home/ggmount/masterDF_july24.pkl'
    new_root='/data/test/'
    outFolder='/home/ggmount/'
    noPortalPath='/data/LSU_noRecord'
    badBarcodePath='/data/LSU_badBarcode'
    rerun=FALSE
    # List files to skip over 
    unwanted=["_m","_s","_l","txt"]

    # Make this directories if needed
    pathlib.Path(noPortalPath).mkdir(parents=True, exist_ok=True) 
    pathlib.Path(badBarcodePath).mkdir(parents=True, exist_ok=True) 

    # Change pkl files to dictionaries
    barcode_dict=pickleOpen(barcode_pkl)
    portal_dict=pickleOpen(portal_pkl)

    newPaths,noLarge,badbarcode,duplicate=moveFiles(new_root,barcode_dict,portal_dict,unwanted,noPortalPath,badBarcodePath,rerun)
    pklDictOut(newPaths,outFolder,'lsu_newPaths_Aug09')
    pklDictOut(noLarge,outFolder,'lsu_noLarge_Aug09')
    pklDictOut(badbarcode,outFolder,'lsu_badBarcode_Aug09')
    pklDictOut(badbarcode,outFolder,'lsu_duplicate_Aug09')

if __name__ == "__main__":
    main()
