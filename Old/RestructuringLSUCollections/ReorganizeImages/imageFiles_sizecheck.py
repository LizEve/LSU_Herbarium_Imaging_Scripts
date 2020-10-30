import os
import itertools
import pickle
import platform

def pklDictOut(outDict,outPath,outFileName):
    # Output dictionaries into pkl files 
    outFile = open(os.path.join(outPath,outFileName+".pkl"),'wb')
    pickle.dump(outDict,outFile)
    outFile.close()


def pathDict(roots,unwanted,wanted):
    '''
    Get dictionary of all image files in root folders 
    Input- root directory, outfolder for pkl files, pkl file names, list of file extentions to ignore
    Output- two dictionaries
    dict1 - filename: [barcode, date, current path]
    dict2 - barcode: [list of absolute paths to all files with barcode]
    '''
    # Set up empty dictionaries d1 = has _L, d2= does not have _L 
    dict1={}
    dict2={}
    # Iterate through root dirs
    for root in roots:
        # Walk through all folders and files. Not using path or subdirs 
        for path, subdirs, files in os.walk(root):
            # Ignore hidden directories as files, those that start with "."
            files = [f for f in files if not f[0] == '.']
            for name in files:
                # Do not keep any files from unwanted list
                if any(x in name for x in unwanted):
                    pass
                else:
                    # Combine path and name
                    p=os.path.join(path,name)
                    # Get barcode from file name 
                    b=name.split(".")[0].split("_")[0].split("-")[0]
                    for w in wanted:
                        # Get large file path 
                        l=os.path.join(path,b+w)
                        # check if file exists 
                        if not os.path.isfile(l):
                            dict2[b]=[p]
                        elif os.path.isfile(l):
                            dict1[b]=[p]
    return dict1,dict2

def main():
    # List unwanted extensions
    unwanted=["txt","tmp","csv","zip","_s","_m","_l","_S","_M","_L"]
    # List wanted extensions 
    wanted=["_L.JPG"]
    # Full path to folder for output lists
    outFolder='/home/ggmount/'
    # Full path of current parent folders of images
    # First look only in vascular 
    #root6 = '/data/LSUCollections/Vascular/'
    root1 = '/data/nfsshare/laf/0'
    
    # Get dictionaries of files and barcodes 
    d1,d2=pathDict([root6],unwanted,wanted)

    # Save dictionaries to pkl files
    pklDictOut(d1,outFolder,'LSU_Vascular_has_L')
    pklDictOut(d2,outFolder,'LSU_Vascular_no_L')

    print("Files with _L = "+str(len(d1)))
    print("Files withOUT _L = "+str(len(d2)))
    
if __name__ == "__main__":
    main()
