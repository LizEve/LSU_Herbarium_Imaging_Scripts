import os
import itertools
import pickle
import platform

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    to transfer this into a human readable date - import datetime then datetime.datetime.fromtimestamp(stat.st_mtime)
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

def pathDict(roots,unwanted):
    '''
    Get dictionary of all image files in root folders 
    Input- root directory, outfolder for pkl files, pkl file names, list of file extentions to ignore
    Output- two dictionaries
    dict1 - filename: [barcode, date, current path]
    dict2 - barcode: [list of absolute paths to all files with barcode]
    '''
    # Set up empty dictionaries
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
                    # get creation or modification date 
                    d=creation_date(p)
                    # Get barcode from file name 
                    b=name.split(".")[0].split("_")[0].split("-")[0]
                    # Put into dictionary dict1
                    dict1[name]=[b,d,p]
    # Make dict 2
    for key,value in dict1.items():
        # Get barcode and path from list of values
        b=value[0]
        p=value[2]
        # if barcode isnt in the dictionary, add it with filepath 
        if b not in dict2:
            dict2[b]=[p]
        # if barcode is in dictionary, append new file path to list of filepaths
        elif b in dict2:
            dict2[b]=[p]+dict2[b]
        else:
            print("This should never happen")
    return dict1,dict2

def pklDictOut(outDict,outPath,outFileName):
    # Output dictionaries into pkl files 
    outFile = open(os.path.join(outPath,outFileName+".pkl"),'wb')
    pickle.dump(outDict,outFile)
    outFile.close()


def main():
    # List unwanted extensions
    unwanted=["txt","tmp","csv","zip"]
    # Full path to folder for output lists
    outFolder='/home/ggmount/'
    # Full path of current parent folders of images
    rootLSUS = '/data/lsu/'
    # Get dictionaries of files and barcodes 
    d1,d2=pathDict([rootLSUS],unwanted)
    # Save dictionaries to pkl files
    pklDictOut(d1,outFolder,'imageFiles_lsu_Aug08_filename')
    pklDictOut(d2,outFolder,'imageFiles_lsu_Aug08_barcode')


if __name__ == "__main__":
    main()
