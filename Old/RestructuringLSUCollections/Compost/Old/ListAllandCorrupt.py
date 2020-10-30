import os
from PIL import Image
import pandas as pd

def corruptImageFinder(allFilesList):
    '''
    Takes list of all absolute paths to files. Checks for image, and corruption. 
    Returns a dictionary of file name: file path. for all corrupted/non image files
    '''
    # Dictionary of files that cannot open as an image
    notImageDict={}
    # Dictionary of files that cannot load as an image, are corrupted
    corruptImageDict={}

    for f in allFilesList:
        # Try opening image. 
        try:
            v_image = Image.open(f)
            # Try loading image
            try:
                    x=v_image.load()
            # If image cannot load, it is corrupted    
            except Exception as e:
                    corruptImageDict[os.path.basename(f)]=f
                    #print(str(e)+f)
        # If image doesnt open as an image, take note
        except IOError as i:
                corruptImageDict[os.path.basename(f)]=f
                #notImageDict[os.path.basename(f)]=f
                #print(str(i)+f)
    return corruptImageDict


def ListFiles(roots,outFolder):
    # Input is list of folders to search through, with "/" at end of path
    # Will output a file for each folder, based on folder name, listing all files 
    unwanted=["_m","_s","txt","_l"]
    for root in roots:
            folderName=root.split("/")[-2]
            oldPathList=[]
            fileNameList=[]
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
                        fileNameList.append(name.upper())
                        oldPathList.append(oldPath)
            # Get dictionary of corrupt images
            corruptImageDict = corruptImageFinder(oldPathList)
            dfBad = pd.DataFrame.from_dict(corruptImageDict,orient='index',columns=['File Path'])
            dfBad.index.name = 'Image File Name'
            dfBad.to_csv(os.path.join(outFolder,(folderName+"_corruptImages.csv")),sep=",")
            # Write out all files 
            with open(os.path.join(outFolder,(folderName+"_list.txt")),"w") as outFile:
                for f in fileNameList:
                    outFile.write(f+"\n")
                    

outFolder='/Users/ChatNoir/Projects/HerbariumRA/'

# Specify full path of current parent folder of images
rootLSU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/'
rootNO = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/no/'
rootNLU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/nlu/'
roots = [rootLSU,rootNO,rootNLU]                    
                    
ListFiles(roots,outFolder)



