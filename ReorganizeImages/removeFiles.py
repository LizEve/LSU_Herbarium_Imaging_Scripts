import os
import itertools
import pickle
import platform
from csv import DictReader

def pickleOpen(p):
    file=open(p,'rb')
    data = pickle.load(file)
    file.close()
    return data

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
    unwanted=["exe"] # adding something random so list isnt empty. 
    # Full path to folder for output lists
    outFolder='/home/ggmount/'
    # Full path of current parent folders of images
    fromFolder = '/data/nfsshare/lsus'
    toFolder = '/data/cbfla_backup/lsus'
    occurrencesFile = '/home/ggmount/LSUSBarcodestoRemove.csv'
    # Get dictionaries of files and barcodes 
    d1,d2=pathDict([fromFolder],unwanted)
    # dict2 - barcode: [list of absolute paths to all files with barcode]
    # make barcodes uppercase 
    D2=dict((k.upper(), v) for k, v in d2.items())

    # REad in Csv file of files we want to move 
    csv_file = open(occurrencesFile, "r")
    catNumList = [row["Barcode"] for row in DictReader(csv_file)]
    L = [x.upper().strip() for x in catNumList]

    # For each record in list to move, find in file path dictionary. 
    for b in L:
        if b in D2:
            print(D2[b])
            for f in D2[b]:
                print(f)
                os.system('mv %s %s' % (f,toFolder))



if __name__ == "__main__":
    main()
