import os
import itertools
import pickle

def pathDict(roots,outFolder,outPkl,unwanted):
    '''
    Get dictionary of all files we want to transfer
    Input- root directory, outfolder for pkl files, pkl file names, list of file extentions to ignore
    Output- dictionary of barcode: [list of absolute paths to all files with barcode]
    '''
    oldPathList=[]
    oldPathDictionary={}
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
        barcode=fileName.split(".")[0].split("_")[0].split("-")[0]
        #print barcode
        # if barcode isnt in the dictionary, add it with file, if it is, add any extra files. 
        if barcode not in oldPathDictionary:
            oldPathDictionary[barcode]=[fileName]
        elif barcode in oldPathDictionary:
            oldPathDictionary[barcode]=[fileName]+oldPathDictionary[barcode]
        else:
            print("This should never happen")
    dictCaps = dict((k.upper(), v) for k, v in oldPathDictionary.items())
    outD = open(os.path.join(outFolder,outPkl+"D.pkl"),'wb')
    outL = open(os.path.join(outFolder,outPkl+"L.pkl"),'wb')
    pickle.dump(dictCaps,outD)
    pickle.dump(oldPathList,outL)
    outD.close()
    outL.close()
    return dictCaps

def main():
    # Specify full path to folder for output lists
    # Specify full path of current parent folder of images
    outFolder1='/home/gmount1/'
    rootLSU = '/data_storage/nfsshare/lsu/'
    rootNO1 = '/data_storage/nfsshare/no/vas_plants/'
    rootNO2 = '/data_storage/nfsshare/no/0/'
    rootNLU = '/data_storage/nfsshare/nlu/'
    rootLSUS = '/data_storage/nfsshare/lsus/'
    cbflaRoots = [rootLSU,rootNO1,rootNO2,rootNLU,rootLSUS]
    outPkl1 = 'cbfla_Jun07'
    unwanted=["txt"]
    fileDict=pathDict(cbflaRoots,outFolder1,outPkl1,unwanted)

    rootLSU = '/data/cbfla_backup/lsu/'
    rootNO1 = '/data/no/vas_plants/'
    rootNO2 = '/data/no/0/'
    rootNLU = '/data/nlu/'
    rootLSUS = '/data/lsus/'
    lsa303Roots = [rootLSU,rootNO1,rootNO2,rootNLU,rootLSUS]
    outFolder2='/home/ggmount/'
    outPkl2 = 'lsa303_Jun07'
    unwanted=["txt","tmp","csv","zip"]
    fileDict=pathDict(lsa303Roots,outFolder2,outPkl2,unwanted)


if __name__ == "__main__":
    main()
