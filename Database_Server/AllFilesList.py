import os
import csv
from csv import DictReader
import itertools
import pathlib2 as pathlib
import shutil
from PIL import Image
import pandas as pd

def oldPathDict(roots):
    '''
    Get dictionary of all files in a folder
    Input- root directory
    Output- dictionary of barcode: [list of file names with barcode]
    Details- does not move any txt, _l, _m, _s, jpg files. Does not specify file extension
    <https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files>
    '''
    oldPathList=[]
    oldPathDictionary={}
    unwanted=["_m","_s","txt","_l","jpg"]
    for root in roots:
        for path, subdirs, files in os.walk(root):
            # Ignore hidden directories as files, those that start with "."
            files = [f for f in files if not f[0] == '.']
            subdirs[:] = [d for d in subdirs if not d[0] == '.']
            for name in files:
                # Do not keep any files from unwanted list
                if any(x in name for x in unwanted):
                    pass
                else:
                    oldPath=os.path.join(path,name)
                    oldPathList.append(oldPath)
    #turn this info into dictionary barcode:all filepaths with barcode
    for oldPath in oldPathList:
        # Get file name and barcode
        fileName=oldPath.split("/")[-1]
        barcode=fileName.split(".")[0].split("_")[0]
        #print barcode
        # if barcode isnt in the dictionary, add it with file, if it is, add any extra files. 
        if barcode not in oldPathDictionary:
            oldPathDictionary[barcode]=[fileName]
        elif barcode in oldPathDictionary:
            oldPathDictionary[barcode]=[fileName]+oldPathDictionary[barcode]
        else:
            print("This should never happen")
    return oldPathDictionary


#rootLSU = '/mnt/c/Users/image/Desktop/gmount/output_fake/LSU/'
rootLSU = '/mnt/j/CFLA-LSU-Station2/images/output/LSU/'
oldRoots = [rootLSU]
oldPathDictionary=oldPathDict(oldRoots)
portalName = 'Vascular_LaCie'
outFolder = '/mnt/c/Users/image/Desktop/gmount/'
# {filename:[barcode,portal,newpath]}
dfFiles = pd.DataFrame.from_dict(oldPathDictionary,orient='index',columns=['File Name'])
dfFiles.index.name = 'Barcode'
dfFiles.to_csv(os.path.join(outFolder,(portalName+"_files.csv")),sep=",")
