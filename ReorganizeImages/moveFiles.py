import pickle 
import os
import itertools
import pathlib2 as pathlib

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

def moveFiles(new_root,barcode_dict,portal_dict,unwanted):

    # Make all barcodes into caps for comparison
    barcode_Dict=dict((k.upper(), v) for k, v in barcode_dict.items())
    portal_Dict=dict((k.upper(), v) for k, v in portal_dict.items())

    # Start dictionary to put new file paths in
    # filename: [barcode, portal, date, current(new) path]
    new_dict={}
    nolarge_dict={}

    # Iterate through every barcode in image barcode dict
    for b in barcode_Dict:

        # Split apart letters and numbers from barcode
        try:
            b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
        except ValueError:
            print("Incorrect barcode format. Excepting only one set of numbers and letters: "+str(b))
        
        # Look for barcode in portal dictionary 
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

                        # Assume paths to old "large" file (which is smaller) for image file
                        lp=str(pathlib.Path(p).with_suffix(""))+str("_l.jpg")
                        lnewPath=str(pathlib.Path(newPath).with_suffix(""))+str("_l.jpg")

                        # Try to copy large file to new location. If no large exists, add to dict of files that need larges
                        try:
                            shutil.copy2(lp,lnewPath)
                        except FileNotFoundError:
                            nolarge_dict[b]=newPath
                    
                        # Get creation date 
                        d = creation_date(p)

                        #filename: [barcode, portal, date, current(new) path]
                        filesMovedDict[fileName]=[b,portal,d,newPath]

                    elif os.path.exists(newPath):
                        print(newPath+" already has a file here. Nothing moved.")
                    
        elif b not in portal_Dict:
            print("Error - image barcode "+str(b)+" not in master portal list")

    return new_dict,nolarge_dict


def main():
    # Read in dictionaries 
    # dict1 - filename: [barcode, date, current path]
    # dict2 - barcode: [list of absolute paths to all files with barcode]
    # portal - barcode: portal
    barcode_pkl='/home/ggmount/imageFiles_lsu_Aug08_barcode.pkl'
    portal_pkl='/home/ggmount/masterDF_july24.pkl'
    new_root='/data/'
    outFolder='/home/ggmount/'
    # List files to skip over 
    unwanted=["_m","_s","_l"]

    # Change pkl files to dictionaries
    barcode_dict=pickleOpen(barcode_pkl)
    portal_dict=pickleOpen(portal_pkl)

    newPaths,noLarge=moveFiles(new_root,barcode_dict,portal_dict,unwanted)
    pklDictOut(newPaths,outFolder,'newPaths_lsu_Aug08')
    pklDictOut(noLarge,outFolder,'noLarge_lsu_Aug08')
    

if __name__ == "__main__":
    main()
