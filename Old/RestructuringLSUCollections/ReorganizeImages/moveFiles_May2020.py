import pickle 
import os
import itertools
import pathlib2 as pathlib
import shutil 
import platform

def pklDictOut(outDict,outPath,outFileName):
    # Output dictionaries into pkl files 
    outFile = open(os.path.join(outPath,outFileName+".pkl"),'wb')
    pickle.dump(outDict,outFile)
    outFile.close()

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

def badBarcodeSequence(p,b,unwanted,badBarcodePath,badbarcode_dict):
    # Ignore files in "unwanted" list 
    if any(x in p for x in unwanted):
        pass

    else:
        # Make new path to folder for images that have a bad barcode 
        fName=os.path.basename(p)
        newPath=os.path.join(badBarcodePath,fName.upper())

        # Copy file, preserving permissions 
        print(newPath)
        shutil.copy2(p,newPath)
    
        # Get creation date 
        d = creation_date(p)

        #filename: [barcode,  date, old path]
        badbarcode_dict[fName]=[b,d,p]
        #print("Incorrect barcode format. Putting files from ,"+str(b)+", into "+str(badBarcodePath))
    return badbarcode_dict
            
def moveFiles(roots,new_root,unwanted,badBarcodePath,barcodeLen,portal):

    # Start dictionary to put new file paths in
    # filename: [barcode, portal, date, current(new) path]
    new_dict={}
    # filename:[barcode,date,old_path]
    badbarcode_dict={}
    
    # Iterate through root dirs
    for root in roots:
        # Walk through all folders and files. 
        for path, subdirs, files in os.walk(root):
            # Ignore hidden directories as files, those that start with "."
            files = [f for f in files if not f[0] == '.']
            for n in files:
                # Do not keep any files from unwanted list
                if any(x in n for x in unwanted):
                    pass
                else:
                    name = n.upper()

                    # Combine path and name

                    p=os.path.join(path,n)

                    # get creation or modification date 

                    d=creation_date(p)

                    # Get barcode from file name 

                    b=name.split(".")[0].split("_")[0].split("-")[0]
                    #print("barcode "+str(b))
                    # if barcode is the right lenght, go through a lot of stuff. 

                    if len(b) == int(barcodeLen):

                        # Split apart letters and numbers from barcode
                        try:
                            b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]

                        # For bad barcodes move them to a special folder for Jennie to check. 
                        except ValueError:
                           badbarcode_dict=badBarcodeSequence(p,b,unwanted,badBarcodePath,badbarcode_dict)
            
                        # For all good barcodes that can be split into Letters/Numbers
                        else:
                            #print(b+", good barcode")
                            try: 
                                # Get new file path and uppercase file name 
                                newDir,newPath,fileName=newPathNames(b,p,new_root,portal)
                                # Check if file exists at new path
                                if not os.path.exists(newPath):
                                    #print(p+", new path")
                                    # Make new directories if needed https://docs.python.org/3/library/pathlib.html
                                    if not os.path.exists(newDir):
                                        pathlib.Path(newDir).mkdir(parents=True, exist_ok=True) 

                                    # Get creation date 
                                    d = creation_date(p)

                                    #filename: [barcode, portal, date, current(new) path]
                                    new_dict[fileName]=[b,portal,d,newPath]

                                    # Copy file, preserving permissions 
                                    print(newPath)
                                    shutil.copy2(p,newPath)

                                # If path exists, also copy 
                                elif os.path.exists(newPath):
                                    #print(p+", duplicate path")
                                    # Copy file, preserving permissions 
                                    print(newPath)
                                    shutil.copy2(p,newPath)
                            except Exception as e: 
                                print(e)
                                badbarcode_dict=badBarcodeSequence(p,b,unwanted,badBarcodePath,badbarcode_dict)
                        # If barcode is wrong lenght, shove it somewhere else, and make note. 
                    else:
                        badbarcode_dict=badBarcodeSequence(p,b,unwanted,badBarcodePath,badbarcode_dict)
    
    return new_dict,badbarcode_dict


def main():
    roots=['/data/cbfla_backup/no/vas_plants/']
    portal="Vascular"
    new_root='/data/LSUCollections/'
    outFolder='/home/ggmount/'
    badBarcodePath='/home/ggmount/BadBarcode/NO/'
    barcodeLen=9
    # List files to skip over 
    unwanted=["_m","_s","_l","txt","_M","_L","_S","thumb","THUMB","Thumb","db","CR2"]
    # Make this directories if needed
    pathlib.Path(badBarcodePath).mkdir(parents=True, exist_ok=True) 

    newPaths,badbarcode = moveFiles(roots,new_root,unwanted,badBarcodePath,barcodeLen,portal)

    pklDictOut(newPaths,outFolder,'no_newPaths_May2020')
    pklDictOut(badbarcode,outFolder,'no_badBarcode_May2020')


if __name__ == "__main__":
    main()
