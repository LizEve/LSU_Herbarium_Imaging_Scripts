import os
import itertools
import pickle

def oldPathDict(roots):
    '''
    Get dictionary of all files we want to transfer
    Input- root directory
    Output- dictionary of barcode: [list of absolute paths to all files with barcode]
    Details- does not move any txt, _l, _m, _s, CR2 files. Does not specify file extension
    <https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files>
    '''
    oldPathList=[]
    oldPathDictionary={}
    barcodeSet=set()
    unwanted=["_m","_s","txt","_l","CR2"]
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
        # SPlit into letters and numbers 
        barcodeSplit = ["".join(x) for _, x in itertools.groupby(barcode, key=str.isdigit)]
        if barcodeSplit[0] == 'LSU':
            print(barcode)
            # if barcode isnt in the dictionary, add it with file, if it is, add any extra files. 
            if barcode not in oldPathDictionary:
                oldPathDictionary[barcode]=[oldPath]
                # add only numbers to list. 
                barcodeSet.add(int(barcodeSplit[1]))
            elif barcode in oldPathDictionary:
                oldPathDictionary[barcode]=[oldPath]+oldPathDictionary[barcode]
            else:
                print("This should never happen")
    return barcodeSet



rootLSU = '/data_storage/nfsshare/lsu/'
#rootLSU = '/Users/ChatNoir/Projects/HerbariumRA/data_storage_fake/nfsshare/lsu/'
#oldRoots = [rootLSU,rootNO,rootNLU]
oldRoots = [rootLSU]

# Get dictionary of current image paths, organized by barcode
# barcode:[filepath1,...filepathN]
barcodeSet = oldPathDict(oldRoots)

numerical = sorted(barcodeSet)

with open('LSUbarcodeList03282019', 'wb') as f:
    pickle.dump(numerical, f)

with open('LSUbarcodeList03282019', 'rb') as f:
    barcodes = pickle.load(f)

a=200000
b=208291
shared=[]
missing=[]

for i in range (a,b):
    if i in barcodes:
        shared.append(i)
    else:
        missing.append(i)
    

with open('MissingBetween200000_208291', 'wb') as f:
    pickle.dump(missing, f)

with open('MissingBetween200000_208291.txt', 'w') as txt:
    for item in missing:
        txt.write("%s\n" % item)