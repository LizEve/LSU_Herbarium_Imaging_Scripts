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

def badBarcodeSequence(p,b,barcode_Dict,unwanted,badBarcodePath,badbarcode_dict,tempDate):
    # Iterate through all file paths in bad barcode dict
    for p in barcode_Dict[b]:

        # Ignore files in "unwanted" list 
        if any(x in p for x in unwanted):
            pass

        else:
            # Make new path to folder for images that have a bad barcode 
            fName=os.path.basename(p)
            newPath=os.path.join(badBarcodePath,fName.upper())
        
            # Get creation date 
            d = creation_date(tempDate)

            #filename: [barcode,  date, old path]
            badbarcode_dict[fName]=[b,d,p]
            #print("Incorrect barcode format. Putting files from ,"+str(b)+", into "+str(badBarcodePath))
    return badbarcode_dict

def moveFiles(new_root,barcode_dict,portal_dict,unwanted,noPortalPath,badBarcodePath,barcodeLen,tempDate):

    # Make all barcodes into caps for comparison
    barcode_Dict=dict((k.upper(), v) for k, v in barcode_dict.items())
    portal_Dict=dict((k.upper(), v) for k, v in portal_dict.items())

    # Start dictionary to put new file paths in
    # filename: [barcode, portal, date, current(new) path]
    new_dict={}
    # filename:newpath(where we want a large image but there is none)
    nolarge_dict={}
    # filename:[barcode,date,old_path]
    badbarcode_dict={}
    # filename:[barcode,date,old_path]
    duplicate_dict={}

    # Iterate through every barcode in image barcode dict
    for b in barcode_Dict:

        # if barcode is the right lenght, go through a lot of stuff. 
        if len(b) == int(barcodeLen):
            # Split apart letters and numbers from barcode
            try:
                b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
                # goodBarcodeSequence(new_root,barcode_dict,portal_dict,unwanted,noPortalPath,badBarcodePath,barcodeLen,tempDate):

            # For bad barcodes move them to a special folder for Jennie to check. 
            except ValueError:
                badbarcode_dict=badBarcodeSequence(p,b,barcode_Dict,unwanted,badBarcodePath,badbarcode_dict,tempDate)
            
            # For all good barcodes that can be split into Letters/Numbers
            else:
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

                            # Get creation date 
                            d = creation_date(tempDate)

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
                            d = creation_date(tempDate)
                            #filename: [barcode, portal, date, current(new) path]
                            new_dict[fileName]=[b,"NoPortal",d,newPath]

        # If barcode is wrong lenght, shove it somewhere else, and make note. 
        else:
            badbarcode_dict=badBarcodeSequence(p,b,barcode_Dict,unwanted,badBarcodePath,badbarcode_dict,tempDate)
    return new_dict,nolarge_dict,badbarcode_dict,duplicate_dict


def main():
    # Read in dictionaries 
    # barcode: [list of absolute paths to all files with barcode]
    # barcode: portal
    barcode_pkl='/Users/ChatNoir/Google Drive/Herbiarum_Notes/ImageSpreadSheets/imageFiles_lsu_Aug08_barcode.pkl'
    portal_pkl='/Users/ChatNoir/Google Drive/Herbiarum_Notes/ImageSpreadSheets/masterDF_july24.pkl'
    new_root='/data/LSUCollections'
    outFolder='/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL'
    noPortalPath='/data/LSUCollections/NoPortal/LSU/'
    badBarcodePath='/data/LSUCollections/BadBarcode/LSU/'
    tempDate='/Users/ChatNoir/Projects/HerbariumRA/Scripts/README.md'
    barcodeLen=11
    # List files to skip over 
    unwanted=["_m","_s","_l","txt"]

    # Change pkl files to dictionaries
    barcode_dict=pickleOpen(barcode_pkl)
    portal_dict=pickleOpen(portal_pkl)

    newPaths,noLarge,badbarcode,duplicate=moveFiles(new_root,barcode_dict,portal_dict,unwanted,noPortalPath,badBarcodePath,barcodeLen,tempDate)
    pklDictOut(newPaths,outFolder,'temp_newPaths_Aug09')
    pklDictOut(noLarge,outFolder,'temp_noLarge_Aug09')
    pklDictOut(badbarcode,outFolder,'temp_badBarcode_Aug09')
    pklDictOut(badbarcode,outFolder,'temp_duplicate_Aug09')

if __name__ == "__main__":
    main()
