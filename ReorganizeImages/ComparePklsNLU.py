import pickle 

def pickleOpen(p):
    file=open(p,'rb')
    data = pickle.load(file)
    file.close()
    return data



# Read in the list of all files before moving  
homeDir='/Users/ChatNoir/Google Drive/Herbiarum_Notes/ImageSpreadSheets/'


dupFiles = pickleOpen(homeDir+'nlu_duplicate_Aug12.pkl')
dupDict = dict((k.upper(), v) for k, v in dupFiles.items())

# Read in the list of files that were moved with good barcodes
goodFiles = pickleOpen(homeDir+'nlu_newPaths_Aug12.pkl')
goodDict = dict((k.upper(), v) for k, v in goodFiles.items())

badFiles = pickleOpen(homeDir+'nlu_badBarcode_Aug12.pkl')
badDict = dict((k.upper(), v) for k, v in badFiles.items())

len(goodDict)
len(goodFiles)

len(badDict)
len(badFiles)

allDict = {**goodDict, **badDict}

set(movedDict).difference(set(allDict))
set(allDict).difference(set(movedDict))

imageFiles = pickleOpen(homeDir+'nlu_imageFiles_Aug12_filename.pkl')
imageDict = dict((k.upper(), v) for k, v in imageFiles.items())

movedFiles = pickleOpen(homeDir+'nlu_movedFiles_Aug13_filename.pkl')
movedDict = dict((k.upper(), v) for k, v in movedFiles.items())
len(movedDict)
len(imageDict)
# All in A, that are not in B 
set(movedDict).difference(set(imageDict))
set(imageDict).difference(set(movedDict))


imageFiles = pickleOpen(homeDir+'nlu_imageFiles_Aug12_barcode.pkl')
imageDict = dict((k.upper(), v) for k, v in imageFiles.items())

movedFiles = pickleOpen(homeDir+'nlu_movedFiles_Aug13_barcode.pkl')
movedDict = dict((k.upper(), v) for k, v in movedFiles.items())

len(movedDict)
len(imageDict)
# All in A, that are not in B 
set(movedDict).difference(set(imageDict))
set(imageDict).difference(set(movedDict))


portal_dict=pickleOpen(homeDir+'masterDF_july24.pkl')
portal_Dict=dict((k.upper(), v) for k, v in portal_dict.items())

portalNLU=splitCollection(portal_Dict,'NLU')
len(portalNLU) # 51885

# All barcodes in portal list that are not in LSU folders
len(set(portalNLU).difference(set(imageDict))) #708 